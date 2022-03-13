import collections, itertools, functools, math
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# 1305 - All Elements in Two Binary Search Trees - MEDIUM
class Solution:
    # result of inorder traversal of a Binary Search Tree is ascending order
    # O((m+n) * log(m+n))
    def getAllElements(self, root1: TreeNode, root2: TreeNode) -> List[int]:
        def dfs(node):
            if node:
                dfs(node.left)
                valueList.append(node.val)
                dfs(node.right)

        valueList = []
        dfs(root1)
        dfs(root2)
        return sorted(valueList)

    # O((m+n) * 2)
    def getAllElements(self, root1: TreeNode, root2: TreeNode) -> List[int]:
        def inorder(node: TreeNode, l: List[int]):
            if not node:
                return
            inorder(node.left, l)
            l.append(node.val)
            inorder(node.right, l)
            return

        l1, l2 = [], []
        inorder(root1, l1)
        inorder(root2, l2)
        ans, i, j = [], 0, 0
        while i < len(l1) or j < len(l2):
            if i < len(l1) and (j == len(l2) or l1[i] <= l2[j]):
                ans.append(l1[i])
                i += 1
            else:
                ans.append(l2[j])
                j += 1
        return ans


# 1306 - Jump Game III - MEDIUM
class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        visited, self.ans = set(), False

        def dfs(idx: int):
            visited.add(idx)
            if 0 <= idx + arr[idx] < len(
                    arr) and idx + arr[idx] not in visited:
                dfs(idx + arr[idx])
            if 0 <= idx - arr[idx] < len(
                    arr) and idx - arr[idx] not in visited:
                dfs(idx - arr[idx])
            if not arr[idx]:
                self.ans = True
            return

        dfs(start)
        return self.ans

    def canReach(self, arr: List[int], start: int) -> bool:
        dq, seen = collections.deque([start]), {start}
        while dq:
            cur = dq.popleft()
            if arr[cur] == 0:
                return True
            for child in cur - arr[cur], cur + arr[cur]:
                if 0 <= child < len(arr) and child not in seen:
                    seen.add(child)
                    dq.append(child)
        return False


# 1314 - Matrix Block Sum - MEDIUM
class Solution:
    def matrixBlockSum(self, mat: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        sums = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                sums[i][j] = sum(mat[i][max(j - k, 0):min(j + k + 1, n)])
        ans = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                ans[i][j] = sum([
                    sums[p][j] for p in range(max(i - k, 0), min(i + k + 1, m))
                ])
        return ans

    def matrixBlockSum(self, mat: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        for i in range(m):
            for j in range(1, n):
                mat[i][j] += mat[i][j - 1]
        for i in range(1, m):
            for j in range(n):
                mat[i][j] += mat[i - 1][j]
        ans = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                r1, c1, r2, c2 = max(0, i - k), max(0, j - k), min(
                    m - 1, i + k), min(n - 1, j + k)
                ans[i][j] = mat[r2][c2] - (
                    mat[r2][c1 - 1]
                    if c1 > 0 else 0) - (mat[r1 - 1][c2] if r1 > 0 else 0) + (
                        mat[r1 - 1][c1 - 1] if r1 > 0 and c1 > 0 else 0)
        return ans

    def matrixBlockSum(self, mat: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        ps = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                ps[i +
                   1][j +
                      1] = mat[i][j] + ps[i][j + 1] + ps[i + 1][j] - ps[i][j]
        ans = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                r1, c1, r2, c2 = max(0, i - k), max(0, j - k), min(
                    m - 1, i + k), min(n - 1, j + k)
                ans[i][j] = ps[r2 + 1][c2 + 1] - ps[r2 + 1][c1] - ps[r1][
                    c2 + 1] + ps[r1][c1]
        return ans

    def matrixBlockSum(self, mat: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        ps = [[0] * (n + 1) for _ in range(m + 1)]
        for i, j in itertools.product(range(m), range(n)):
            ps[i + 1][j +
                      1] = mat[i][j] + ps[i][j + 1] + ps[i + 1][j] - ps[i][j]
        ans = [[0] * n for _ in range(m)]
        for i, j in itertools.product(range(m), range(n)):
            r1, c1, r2, c2 = max(0, i - k), max(0,
                                                j - k), min(m, i + k + 1), min(
                                                    n, j + k + 1)
            ans[i][j] = ps[r2][c2] - ps[r2][c1] - ps[r1][c2] + ps[r1][c1]
        return ans


# 1325 - Delete Leaves With a Given Value - MEDIUM
class Solution:
    def removeLeafNodes(self, root: TreeNode, target: int) -> TreeNode:
        def postorder(root):
            if not root:
                return None
            if postorder(root.left) and root.left.val == target:
                root.left = None
            if postorder(root.right) and root.right.val == target:
                root.right = None
            if not root.left and not root.right:
                return True
            return False

        postorder(root)
        return None if root.val == target and root.right == root.left == None else root

    def removeLeafNodes(self, root: TreeNode, target: int) -> TreeNode:
        if root.left:
            root.left = self.removeLeafNodes(root.left, target)
        if root.right:
            root.right = self.removeLeafNodes(root.right, target)
        return None if root.left == root.right and root.val == target else root

    def removeLeafNodes(self, root, target):
        if root:
            root.left = self.removeLeafNodes(root.left, target)
            root.right = self.removeLeafNodes(root.right, target)
            if root.val != target or root.left or root.right:
                return root


# 1332 - Remove Palindromic Subsequences - EASY
class Solution:
    def removePalindromeSub(self, s: str) -> int:
        return 1 if s == s[::-1] else 2


# 1342 - Number of Steps to Reduce a Number to Zero - EASY
class Solution:
    def numberOfSteps(self, num: int) -> int:
        step = 0
        while num:
            if num & 1:
                num -= 1
            else:
                num //= 2
            step += 1
        return step


# 1345 - Jump Game IV - HARD
class Solution:
    # O(n) / O(n)
    def minJumps(self, arr: List[int]) -> int:
        n = len(arr)
        idx = collections.defaultdict(list)
        # save left and right endpoints of the interval with the same value appearing consecutively
        for i in range(n):
            if i in (0, n - 1):
                idx[arr[i]].append(i)
            elif arr[i] != arr[i - 1] or arr[i] != arr[i + 1]:
                idx[arr[i]].append(i)
        visited = [True] + [False] * (n - 1)
        dq = collections.deque([(0, 0)])
        while dq:
            i, step = dq.popleft()
            for j in (idx.get(arr[i], []) + [i - 1, i + 1]):
                if 0 <= j < n and not visited[j]:
                    if j == n - 1:
                        return step + 1
                    visited[j] = True
                    dq.append((j, step + 1))
            idx[arr[i]] = []  # has visited
        return 0

    def minJumps(self, arr: List[int]) -> int:
        g = collections.defaultdict(list)
        n = len(arr)
        for i in range(n):
            g[arr[i]].append(i)
        dq = collections.deque([(0, 0)])
        seen = set([0])
        while dq:
            i, step = dq.popleft()
            if i == n - 1:
                return step
            for nxt in g[arr[i]] + [i - 1, i + 1]:
                if 0 <= nxt < n and nxt not in seen:
                    seen.add(nxt)
                    dq.append((nxt, step + 1))
            del g[arr[i]]
        return -1

    def minJumps(self, arr: List[int]) -> int:
        g = collections.defaultdict(list)
        shorter = []
        size = 0
        # remove the consecutive repeated value in the 'arr'
        for i, v in enumerate(arr):
            if 0 < i < len(arr) - 1 and v == arr[i - 1] and v == arr[i + 1]:
                continue
            else:
                g[v].append(size)
                shorter.append(v)
                size += 1
        arr = shorter
        visited = {0}
        q = collections.deque([(0, 0)])
        while q:
            idx, step = q.popleft()
            if idx == size - 1:
                return step
            value = arr[idx]
            for j in g[value] + [idx - 1, idx + 1]:
                if 0 <= j < size and j not in visited:
                    q.append((j, step + 1))
                    visited.add(j)
            del g[value]
        return 0


# 1380 - Lucky Numbers in a Matrix - EASY
class Solution:
    def luckyNumbers(self, matrix: List[List[int]]) -> List[int]:
        ans = []
        colmax = {}
        m, n = len(matrix), len(matrix[0])
        for j in range(n):
            for i in range(m):
                if matrix[i][j] > colmax.get(j, 0):
                    colmax[j] = matrix[i][j]
        s = set(colmax.values())
        for i in range(m):
            rowmin = math.inf
            for j in range(n):
                if matrix[i][j] < rowmin:
                    rowmin = matrix[i][j]
            if rowmin in s:
                ans.append(rowmin)
        return ans

    def luckyNumbers(self, matrix: List[List[int]]) -> List[int]:
        minRow = [min(row) for row in matrix]
        maxCol = [max(col) for col in zip(*matrix)]
        ans = []
        for i, row in enumerate(matrix):
            for j, x in enumerate(row):
                if x == minRow[i] == maxCol[j]:
                    ans.append(x)
        return ans

    def luckyNumbers(self, matrix: List[List[int]]) -> List[int]:
        ans = []
        cols = list(zip(*matrix))
        for rows in matrix:
            num = min(rows)
            c = rows.index(num)
            if max(cols[c]) == num:
                ans.append(num)
        return ans


# 1381 - Design a Stack With Increment Operation - MEDIUM
class CustomStack:
    def __init__(self, maxSize: int):
        self.m = maxSize
        self.l = 0
        self.s = []

    def push(self, x: int) -> None:
        if self.l < self.m:
            self.s.append(x)
            self.l += 1

    def pop(self) -> int:
        if self.s:
            r = self.s.pop()
            self.l -= 1
            return r
        return -1

    # O(k)
    def increment(self, k: int, val: int) -> None:
        i = 0
        while i < k and i < self.l:
            self.s[i] += val
            i += 1


class CustomStack:
    def __init__(self, maxSize: int):
        self.stk = [0] * maxSize
        self.add = [0] * maxSize
        self.top = -1

    def push(self, x: int) -> None:
        if self.top < len(self.stk) - 1:
            self.top += 1
            self.stk[self.top] = x

    def pop(self) -> int:
        if self.top == -1:
            return -1
        ret = self.stk[self.top] + self.add[self.top]
        if self.top != 0:
            self.add[self.top - 1] += self.add[self.top]
        self.add[self.top] = 0
        self.top -= 1
        return ret

    def increment(self, k: int, val: int) -> None:
        l = min(k - 1, self.top)
        if l >= 0:
            self.add[l] += val