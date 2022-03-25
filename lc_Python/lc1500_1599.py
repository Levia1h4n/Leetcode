from typing import List
import collections, functools, itertools, heapq, math


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# 1518 - Water Bottles - EASY
class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        ans, empty = 0, 0
        while numBottles:
            ans += numBottles
            numBottles, empty = divmod(empty + numBottles, numExchange)
        return ans


# 1523 - Count Odd Numbers in an Interval Range - EASY
class Solution:
    def countOdds(self, low: int, high: int) -> int:
        d = high - low + 1
        if d & 1:
            return d // 2 + 1 if high & 1 else d // 2
        return d // 2

    def countOdds(self, low: int, high: int) -> int:
        # the number of odd numbers before this one
        pre = lambda x: (x + 1) >> 1
        return pre(high) - pre(low - 1)


###############
# 2022.1.6 VO #
###############
# 1530 - Number of Good Leaf Nodes Pairs - MEDIUM
class Solution:
    # postorder
    def countPairs(self, root: TreeNode, distance: int) -> int:
        def dfs(root: TreeNode) -> List[int]:
            if not root:
                return []
            if root.left is None and root.right is None:
                return [1]
            left = dfs(root.left)
            right = dfs(root.right)
            for l in left:
                for r in right:
                    if l + r <= distance:
                        self.ans += 1
            return [x + 1 for x in left + right]
            return [x + 1 for x in left + right if x + 1 < distance]  # prune

        self.ans = 0
        dfs(root)
        return self.ans


# 1567 - Maximum Length of Subarray With Positive Product - MEDIUM
class Solution:
    # dp
    def getMaxLen(self, nums: List[int]) -> int:
        n = len(nums)
        pos, neg = [0] * n, [0] * n
        if nums[0] > 0: pos[0] = 1
        if nums[0] < 0: neg[0] = 1
        ans = pos[0]
        for i in range(1, n):
            if nums[i] > 0:
                pos[i] = 1 + pos[i - 1]
                neg[i] = 1 + neg[i - 1] if neg[i - 1] > 0 else 0
            elif nums[i] < 0:
                pos[i] = 1 + neg[i - 1] if neg[i - 1] > 0 else 0
                neg[i] = 1 + pos[i - 1]
            ans = max(ans, pos[i])
        return ans

    def getMaxLen(self, nums: List[int]) -> int:
        n = len(nums)
        pos, neg = 0, 0
        if nums[0] > 0: pos = 1
        if nums[0] < 0: neg = 1
        ans = pos
        for i in range(1, n):
            if nums[i] > 0:
                pos = 1 + pos
                neg = 1 + neg if neg > 0 else 0
            elif nums[i] < 0:
                pos, neg = 1 + neg if neg > 0 else 0, 1 + pos
                # neg = 1 + pos
            else:
                pos = neg = 0
            ans = max(ans, pos)
        return ans

    # sliding window
    def getMaxLen(self, nums: List[int]) -> int:
        nums = [0] + nums + [0]
        last_zero, ans, negs = 0, 0, []  # negative number postion
        for i in range(1, len(nums)):
            if nums[i] == 0:
                if len(negs) % 2 == 0:
                    ans = max(ans, i - last_zero - 1)
                else:
                    ans = max(ans, i - negs[0] - 1, negs[-1] - last_zero - 1)
                last_zero = i
                negs = []
            elif nums[i] < 0:
                negs.append(i)
        return ans


# 1570 - Dot Product of Two Sparse Vectors - MEDIUM
class SparseVector:
    def __init__(self, nums: List[int]):
        self.nums = {k: num for k, num in enumerate(nums) if num != 0}

    def dotProduct(self, vec: 'SparseVector') -> int:
        ans = 0
        for key, value in self.nums.items():
            if key in vec.nums:
                ans += value * vec.nums[key]
        return ans


# 1576 - Replace All ?'s to Avoid Consecutive Repeating Characters - EASY
class Solution:
    def modifyString(self, s: str) -> str:
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        s = ['#'] + list(s) + ['#']
        for i in range(1, len(s) - 1):
            if s[i] == '?':
                new = i
                while s[i - 1] == alpha[new % 26] or s[i + 1] == alpha[new %
                                                                       26]:
                    new += 1
                s[i] = alpha[new % 26]
        return ''.join(s[1:-1])

    def modifyString(self, s: str) -> str:
        alpha = 'abc'
        s = ['#'] + list(s) + ['#']
        for i in range(1, len(s) - 1):
            if s[i] == '?':
                for ch in alpha:
                    if s[i - 1] != ch and s[i + 1] != ch:
                        s[i] = ch
                        break
        return ''.join(s[1:-1])