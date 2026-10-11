"""Judge harness for the LeetCode-style runner on the site.

The same file runs in two places:
- in the browser, inside Pyodide in a Web Worker (inlined by site/build.py), and
- in CPython at build time, where build.py runs every reference solution in
  data/judge/solutions/ through it and refuses to build if one fails.

judge(src, spec_json, report) compiles the student's code once, then calls
Solution().<method>(*args) for each test. report() receives a JSON string per
event: {"start": i} before a test and {"result": {...}} after it, so the page
knows which test was running if it has to kill the worker for a time limit.
Standard library only.
"""
import sys, io, json, time, traceback, copy
from collections import deque

sys.setrecursionlimit(20000)

PRELUDE = """from typing import *
from collections import *
from heapq import *
from math import *
from bisect import *
from itertools import *
from functools import *
import collections, heapq, math, bisect, itertools, functools, string, re
"""
MAX_NODES = 200000
SHOW_LIMIT = 300


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return "ListNode(%r)" % (self.val,)


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return "TreeNode(%r)" % (self.val,)


def list_to_linked(a):
    dummy = tail = ListNode()
    for v in a:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def linked_to_list(head):
    out = []
    while head is not None:
        if not isinstance(head, ListNode):
            raise TypeError("expected a ListNode or None, got %s" % type(head).__name__)
        out.append(head.val)
        if len(out) > MAX_NODES:
            raise ValueError("the returned linked list has a cycle")
        head = head.next
    return out


def list_to_tree(a):
    """LeetCode level order: [3,9,20,null,null,15,7]."""
    if not a or a[0] is None:
        return None
    it = iter(a[1:])
    root = TreeNode(a[0])
    q = deque([root])
    while q:
        node = q.popleft()
        for side in ("left", "right"):
            try:
                v = next(it)
            except StopIteration:
                return root
            if v is not None:
                child = TreeNode(v)
                setattr(node, side, child)
                q.append(child)
    return root


def tree_to_list(root):
    out, q, seen = [], deque([root]), 0
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
            continue
        if not isinstance(node, TreeNode):
            raise TypeError("expected a TreeNode or None, got %s" % type(node).__name__)
        seen += 1
        if seen > MAX_NODES:
            raise ValueError("the returned tree has a cycle")
        out.append(node.val)
        q.append(node.left)
        q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


CONV_IN = {"ListNode": list_to_linked, "TreeNode": list_to_tree}
CONV_OUT = {"ListNode": linked_to_list, "TreeNode": tree_to_list}


def same(got, want):
    if isinstance(want, bool) or isinstance(got, bool):
        return got is want
    if isinstance(want, list):
        return (isinstance(got, (list, tuple)) and len(got) == len(want)
                and all(same(g, w) for g, w in zip(got, want)))
    if isinstance(want, float) or isinstance(got, float):
        return isinstance(got, (int, float)) and abs(got - want) <= 1e-5 * max(1.0, abs(want))
    return type(got) is type(want) and got == want


def show(v):
    try:
        s = json.dumps(v, separators=(",", ":"), ensure_ascii=False)
    except (TypeError, ValueError):
        s = repr(v)
    return s if len(s) <= SHOW_LIMIT else s[:SHOW_LIMIT] + "…"


def fmt_exc(e):
    if isinstance(e, SyntaxError):
        text = (e.text or "").rstrip("\n")
        caret = " " * max((e.offset or 1) - 1, 0) + "^"
        return "%s (line %s): %s\n    %s\n    %s" % (type(e).__name__, e.lineno or "?", e.msg, text, caret)
    lines = [f.lineno for f in traceback.extract_tb(e.__traceback__) if f.filename == "<solution>"]
    where = " (line %d)" % lines[-1] if lines else ""
    msg = str(e)
    if isinstance(e, RecursionError):
        msg += ". Is there a base case that stops the recursion?"
    return "%s%s: %s" % (type(e).__name__, where, msg)


def starter(spec):
    head = ""
    used = set(spec.get("types", [])) | {spec.get("ret")}
    if "ListNode" in used:
        head += ("# Definition for singly-linked list.\n# class ListNode:\n"
                 "#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\n")
    if "TreeNode" in used:
        head += ("# Definition for a binary tree node.\n# class TreeNode:\n"
                 "#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n"
                 "#         self.left = left\n#         self.right = right\n")
    return head + "class Solution:\n    " + spec["sig"] + "\n        "


def _capture(fn, out):
    old = sys.stdout
    sys.stdout = out
    try:
        return fn()
    finally:
        sys.stdout = old


def run_one(cls, spec, t):
    env = {"__builtins__": __builtins__}
    args = eval(t["gen"], env) if "gen" in t else copy.deepcopy(t["args"])
    want = eval(t["expectGen"], env) if "expectGen" in t else t["expected"]
    types = spec.get("types", [])
    args = [CONV_IN[ty](a) if ty in CONV_IN else a for a, ty in zip(args, types + [None] * len(args))]
    out = io.StringIO()
    t0 = time.perf_counter()
    try:
        got = _capture(lambda: getattr(cls(), spec["method"])(*args), out)
        ms = (time.perf_counter() - t0) * 1000
        conv = CONV_OUT.get(spec.get("ret"))
        if conv:
            got = conv(got)
    except BaseException as e:
        return {"ok": False, "status": "RE", "error": fmt_exc(e), "stdout": out.getvalue()[:2000]}
    ok = same(got, want)
    return {"ok": ok, "status": "OK" if ok else "WA", "got": show(got), "want": show(want),
            "ms": round(ms), "stdout": out.getvalue()[:2000]}


def judge(src, spec_json, report):
    spec = json.loads(spec_json)
    stop = spec.get("stopOnFail", True)
    try:
        code = compile(src, "<solution>", "exec")
    except SyntaxError as e:
        return json.dumps({"verdict": "CE", "error": fmt_exc(e)})
    ns = {"__name__": "__main__"}
    exec(PRELUDE, ns)
    ns.update(ListNode=ListNode, TreeNode=TreeNode)
    out = io.StringIO()
    try:
        _capture(lambda: exec(code, ns), out)
    except BaseException as e:
        return json.dumps({"verdict": "RE", "error": fmt_exc(e), "stdout": out.getvalue()[:2000]})
    cls = ns.get("Solution")
    if not isinstance(cls, type):
        return json.dumps({"verdict": "RE", "error": "NameError: class Solution is not defined. Keep the line 'class Solution:'."})
    if not callable(getattr(cls, spec["method"], None)):
        return json.dumps({"verdict": "RE", "error": "AttributeError: Solution has no method '%s'. Keep the signature: %s"
                           % (spec["method"], spec["sig"])})
    verdict, passed = "AC", 0
    total = sum(1 for t in spec["tests"] if not t.get("extra"))
    for i, t in enumerate(spec["tests"]):
        if t.get("extra") and verdict != "AC":
            continue
        report(json.dumps({"start": i}))
        r = run_one(cls, spec, t)
        r["i"] = i
        report(json.dumps({"result": r}))
        if t.get("extra"):
            continue
        if r["ok"]:
            passed += 1
        elif verdict == "AC":
            verdict = r["status"]
            if stop:
                break
    return json.dumps({"verdict": verdict, "passed": passed, "total": total})
