from typing import List, Optional
import collections, math, functools, bisect, heapq, random


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# 300 - Longest Increasing Subsequence - MEDIUM
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[i] > nums[j] and dp[i] < dp[j] + 1:
                    dp[i] = dp[j] + 1
        return max(dp)

    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = []
        for num in nums:
            idx = bisect.bisect_left(dp, num)
            if idx == len(dp):
                dp.append(num)
            else:
                dp[idx] = num
        return len(dp)

    def lengthOfLIS(self, nums: List[int]) -> int:
        dp, ans = [1] * len(nums), 0
        for num in nums:
            lo, hi = 0, ans
            while lo < hi:
                mid = lo + hi >> 1
                if dp[mid] < num:
                    lo = mid + 1
                else:
                    hi = mid
            if lo == len(dp):
                dp.append(num)
            else:
                dp[lo] = num
            if lo == ans:
                ans += 1
        return ans


# 301 - Remove Invalid Parentheses - HARD
class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        l = r = 0
        for c in s:
            if c == '(':
                l += 1
            elif c == ')':
                if l:
                    l -= 1
                else:
                    r += 1
        ans = []
        # cl cr: left or right count
        # dl dr: left or right remain
        @functools.lru_cache(None)
        def dfs(idx, cl, cr, dl, dr, path):
            if idx == len(s):
                if not dl and not dr:
                    ans.append(path)
                return
            if cr > cl or dl < 0 or dr < 0:
                return
            ch = s[idx]
            if ch == '(':
                dfs(idx + 1, cl, cr, dl - 1, dr, path)
            elif ch == ')':
                dfs(idx + 1, cl, cr, dl, dr - 1, path)
            dfs(idx + 1, cl + (ch == '('), cr + (ch == ')'), dl, dr, path + ch)

        dfs(0, 0, 0, l, r, "")
        return ans


# 306 - Additive Number - MEDIUM
class Solution:
    def isAdditiveNumber(self, num: str) -> bool:
        for i in range(1, len(num)):
            for j in range(i + 1, len(num)):
                first, second, remaining = num[:i], num[i:j], num[j:]
                if (first.startswith('0')
                        and first != '0') or (second.startswith('0')
                                              and second != '0'):
                    continue
                while remaining:
                    third = str(int(first) + int(second))
                    if not remaining.startswith(third):
                        break
                    first = second
                    second = third
                    remaining = remaining[len(third):]
                if not remaining:
                    return True
        return False

    def isAdditiveNumber(self, num: str) -> bool:
        def check(i, j):
            a = num[:i + 1]
            b = num[i + 1:j + 1]
            if (a.startswith('0') and a != '0') or (b.startswith('0')
                                                    and b != '0'):
                return False
            c = str(int(a) + int(b))
            temp = a + b + c
            while len(temp) <= len(num):
                if num == temp:
                    return True
                b, c = c, str(int(b) + int(c))
                temp += c
            return False

        for j in range(1, len(num) - 1):
            for i in range(j):
                if check(i, j):
                    return True
        return False


# 309 - Best Time to Buy and Sell Stock with Cooldown - MEDIUM
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        n = len(prices)
        f0, f1, f2 = -prices[0], 0, 0
        for i in range(1, n):
            f0, f1, f2 = max(f0, f2 - prices[i]), f0 + prices[i], max(f1, f2)
            # newf0 = max(f0, f2 - prices[i])
            # newf1 = f0 + prices[i]
            # newf2 = max(f1, f2)
            # f0, f1, f2 = newf0, newf1, newf2
        return max(f1, f2)


# 310 - Minimum Height Trees - MEDIUM
class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if not edges:
            return [0]
        graph = collections.defaultdict(set)
        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)
        leaves, degree = [], []
        for i in range(n):
            if len(graph[i]) == 1:
                leaves.append(i)
            degree.append(len(graph[i]))
        while n > 2:
            new_leaves = []
            for leaf in leaves:
                for adj in graph[leaf]:
                    degree[adj] -= 1
                    if degree[adj] == 1:
                        new_leaves.append(adj)
            n -= len(leaves)
            leaves = new_leaves
        return leaves


# 312 - Burst Balloons - HARD
class Solution:
    # not pass
    @functools.lru_cache(None)
    def maxCoins(self, nums: List[int]) -> int:
        def backtrack(nums: List[int], cur):
            if len(nums) == 0:
                self.ans = max(self.ans, cur)
                return
            for i in range(len(nums)):
                left = nums[i - 1] if i - 1 >= 0 else 1
                right = nums[i + 1] if i + 1 < len(nums) else 1
                cur += left * nums[i] * right
                backtrack(nums[:i - 1] + nums[i + 1:], cur)
            return

        nums = [n for n in nums if n]
        self.ans = -math.inf
        backtrack(nums[1:-1], 0)
        return self.ans

    def maxCoins(self, A: List[int]) -> int:
        # a test case that all elements are '100'
        if len(A) > 1 and len(set(A)) == 1:
            return (A[0]**3) * (len(A) - 2) + A[0]**2 + A[0]
        A, n = [1] + A + [1], len(A) + 2
        dp = [[0] * n for _ in range(n)]
        # why bottom to up: must solve subquestion first
        for i in range(n - 2, -1, -1):
            for j in range(i + 2, n):
                dp[i][j] = max(A[i] * A[k] * A[j] + dp[i][k] + dp[k][j]
                               for k in range(i + 1, j))
        return dp[0][n - 1]

    def maxCoins(self, nums: List[int]) -> int:
        if len(nums) > 1 and len(set(nums)) == 1:  # speed up
            return (nums[0]**3) * (len(nums) - 2) + nums[0]**2 + nums[0]
        nums = [1] + nums + [1]
        # or: nums = [1] + [n for n in nums if n] + [1]
        dp = [[0] * len(nums) for _ in range(len(nums))]
        for i in range(len(nums) - 1, -1, -1):
            for j in range(i + 2, len(nums)):
                for k in range(i + 1, j):
                    dp[i][j] = max(
                        dp[i][j],
                        dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])
        return dp[0][-1]

    def maxCoins(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        elif len(set(nums)) == 1:
            n = nums[0]
            return n**3 * (len(nums) - 2) + n * n + n
        nums = [1] + [n for n in nums if n] + [1]
        N = len(nums)

        @functools.lru_cache(None)
        def helper(lo, hi):
            if lo > hi:
                return 0
            res = -math.inf
            for i in range(lo, hi + 1):
                gain = nums[i] * nums[lo - 1] * nums[hi + 1]
                res = max(res, gain + helper(lo, i - 1) + helper(i + 1, hi))
            return res

        return helper(1, N - 2)


# 314 - Binary Tree Vertical Order Traversal - MEDIUM
# dfs
class Solution:
    def verticalOrder(self, root: TreeNode) -> List[List[int]]:
        # Use a dict to store our answers, keys will be column idxs.
        ans = collections.defaultdict(list)

        def dfs(node, row, col) -> None:
            if not node:
                return
            # Append node vals to column in our dict.
            ans[col].append((row, node.val))
            # Traverse l and r.
            dfs(node.left, row + 1, col - 1)
            dfs(node.right, row + 1, col + 1)
            return

        dfs(root, 0, 0)
        # Sort our dict by keys (column vals)
        ans = dict(sorted(ans.items()))
        ret = []
        # Loop through our sorted dict appending vals sorted by height (top down order).
        for _, v in ans.items():
            ret.append([x[1] for x in sorted(v, key=lambda x: x[0])])
        return ret


# bfs
class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        nodes = collections.defaultdict(list)
        queue = collections.deque([(root, 0)])
        while queue:
            node, pos = queue.popleft()
            if node:
                nodes[pos].append(node.val)
                queue.append((node.left, pos - 1))
                queue.append((node.right, pos + 1))
        # sorted the keys of defaultdict
        return [nodes[i] for i in sorted(nodes)]


# 318 - Maximum Product of Word Lengths - MEDIUM
class Solution:
    def maxProduct(self, words: List[str]) -> int:
        s = [set(x) for x in words]
        maxL = 0
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                if len(s[i].intersection(s[j])) == 0:
                    maxL = max(maxL, len(words[i]) * len(words[j]))
        return maxL


# 319 - Bulb Switcher - MEDIUM
class Solution:
    def bulbSwitch(self, n: int) -> int:
        ans, i = 0, 1
        while i * i <= n:
            i += 1
            ans += 1
        return ans


class Solution:
    def bulbSwitch(self, n: int) -> int:
        return int(math.sqrt(n))


# 322 - Coin Change - MEDIUM
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [0] + [float('inf')] * amount
        for i in range(1, amount + 1):
            dp[i] = min(dp[i - c] if i - c >= 0 else float('inf')
                        for c in coins) + 1
        return dp[-1] if dp[-1] != float('inf') else -1

    def coinChange(self, coins, amount):
        dp = [0] + [float('inf')] * amount
        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] = min(dp[i], dp[i - coin] + 1)
        return dp[-1] if dp[-1] != float('inf') else -1

    def coinChange(self, coins: List[int], amount: int) -> int:
        ans, dq, visited = 0, collections.deque([amount]), set()
        while dq:
            for _ in range(len(dq)):
                val = dq.popleft()
                if val == 0:
                    return ans
                for coin in coins:
                    if val >= coin and val - coin not in visited:
                        visited.add(val - coin)
                        dq.append(val - coin)
            ans += 1
        return -1

    def coinChange(self, coins: List[int], amount: int) -> int:
        @functools.lru_cache(None)
        def dp(amount: int) -> int:
            if amount == 0:
                return 0
            ans = math.inf
            for coin in coins:
                if amount >= coin:
                    ans = min(ans, dp(amount - coin) + 1)
            return ans

        ans = dp(amount)
        return ans if ans != math.inf else -1

    def coinChange(self, coins: List[int], amount: int) -> int:
        @functools.lru_cache(None)
        def dp(amount: int) -> int:
            if amount == 0: return 0
            if amount < 0: return float("inf")
            return min(dp(amount - coin) + 1 for coin in coins)

        return dp(amount) if dp(amount) != float("inf") else -1


# 328 - Odd Even Linked List - MEDIUM
# O(n) / O(n)
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        num = 1
        odd, even = ListNode(-1), ListNode(-1)
        cpodd, cpeven = odd, even
        while head:
            if num & 1:
                odd.next = ListNode(head.val)
                odd = odd.next
            else:
                even.next = ListNode(head.val)
                even = even.next
            head = head.next
            num += 1
        odd.next = cpeven.next
        return cpodd.next


# O(1) / O(n)
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return head
        odd, even = head, head.next
        evenHead = even
        while even and even.next:
            odd.next = odd.next.next
            even.next = even.next.next
            odd = odd.next
            even = even.next
        odd.next = evenHead
        return head


# 334 - Increasing Triplet Subsequence - MEDIUM
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        if len(nums) < 3: return False
        first, second = float('inf'), float('inf')
        for n in nums:
            if n <= first:
                first = n
            elif first < n <= second:
                second = n
            elif n > second:
                return True
        return False


# 337 - House Robber III - MEDIUM
# recursive
class Solution:
    memory = {}

    def rob(self, root: TreeNode) -> int:
        if root is None:
            return 0
        if root.left is None and root.right is None:
            return root.val
        if self.memory.get(root) is not None:
            return self.memory[root]
        # rob root
        val1 = root.val
        if root.left:
            val1 += self.rob(root.left.left) + self.rob(root.left.right)
        if root.right:
            val1 += self.rob(root.right.left) + self.rob(root.right.right)
        # not rob root
        val2 = self.rob(root.left) + self.rob(root.right)
        self.memory[root] = max(val1, val2)
        return max(val1, val2)


# dp
class Solution:
    def rob(self, root: TreeNode) -> int:
        result = self.rob_tree(root)
        return max(result[0], result[1])

    def rob_tree(self, node: TreeNode) -> int:
        if node is None:
            return (0, 0)  # (rob this node，not rob this node)
        left = self.rob_tree(node.left)
        right = self.rob_tree(node.right)
        val1 = node.val + left[1] + right[1]  # rob node
        val2 = max(left[0], left[1]) + max(right[0],
                                           right[1])  # not rob this node
        return (val1, val2)


# 338


# 339 - Nested List Weight Sum - MEDIUM
class NestedInteger:
    def __init__(self, value=None):
        """
       If value is not specified, initializes an empty list.
       Otherwise initializes a single integer equal to value.
       """

    def isInteger(self):
        """
       @return True if this NestedInteger holds a single integer, rather than a nested list.
       :rtype bool
       """

    def getInteger(self):
        """
       @return the single integer that this NestedInteger holds, if it holds a single integer
       Return None if this NestedInteger holds a nested list
       :rtype int
       """

    def getList(self):
        """
       @return the nested list that this NestedInteger holds, if it holds a nested list
       Return None if this NestedInteger holds a single integer
       :rtype List[NestedInteger]
       """


# dfs
class Solution:
    def depthSum(self, nestedList: List[NestedInteger]) -> int:
        self.ans = 0

        def dfs(nestedList: List[NestedInteger], depth: int):
            if not nestedList:
                return
            for i in nestedList:
                if i.isInteger():
                    self.ans += i.getInteger() * depth
                else:
                    dfs(i.getList(), depth + 1)

        dfs(nestedList, 1)
        return self.ans


# bfs
class Solution:
    def depthSum(self, nestedList: List[NestedInteger]) -> int:
        ans, depth = 0, 1
        stack = collections.deque([nestedList])
        while stack:
            for _ in range(len(stack)):
                n = stack.popleft()
                for i in n:
                    if i.isInteger():
                        ans += i.getInteger() * depth
                    else:
                        stack.append(i.getList())
            depth += 1
        return ans


'''
flatten trick about a list of lists
>>> sum([[1, 2], [2, 4]], [])
[1, 2, 2, 4]
'''


class Solution(object):
    def depthSum(self, nestedList):
        depth, ret = 1, 0
        while nestedList:
            ret += depth * sum(
                [x.getInteger() for x in nestedList if x.isInteger()])
            nestedList = sum(
                [x.getList() for x in nestedList if not x.isInteger()], [])
            depth += 1
        return ret


# 343 - Integer Break - MEDIUM
class Solution:
    def integerBreak(self, n: int) -> int:
        dp = [0] * (n + 1)
        for i in range(2, n + 1):
            for j in range(i):
                dp[i] = max(dp[i], j * (i - j), j * dp[i - j])
        return dp[n]

    def integerBreak(self, n: int) -> int:
        if n <= 3:
            return n - 1
        d, mod = n // 3, n % 3
        if mod == 0:
            return 3**d
        if mod == 1:
            return 3**(d - 1) * 4
        return 3**d * 2


# 344 - Reverse String - EASY
class Solution:
    def reverseString(self, s: List[str]) -> None:
        for i in range(len(s) // 2):
            s[i], s[-i - 1] = s[-i - 1], s[i]
        # s[:] = s[::-1]
        # s.reverse()
        return


# 345

# 346


# 347 - Top K Frequent Elements - MEDIUM
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        cnt = collections.Counter(nums)
        # sorted by value and get the key
        return [i[0] for i in sorted(cnt.items(), key=lambda x: x[1])[-k:]]
        # return [i[0] for i in sorted(cnt.items(), key=lambda x: x[1], reverse=True)[:k]]


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        cnt = collections.Counter(nums)
        # convert to 'tuple' to sort, because 'dict' is unordered
        times = sorted(cnt.items(), key=lambda k: k[1])
        ans = []
        while k != 0 and len(times) > 0:
            ans.append(times.pop()[0])
            k -= 1
        return ans


# 349 - Intersection of Two Arrays - EASY
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        return set(nums1).intersection(set(nums2))


# 367 - Valid Perfect Square - EASY
# binary search
class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        left, right = 0, num
        while left <= right:
            mid = (left + right) // 2
            if mid * mid > num:
                right = mid - 1
            elif mid * mid < num:
                left = mid + 1
            else:
                return True
        return False


# math: sum of odd -> 1+3+5+7+... = n^2
#       (n+1)^2 - n^2 = 2n+1
class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        odd = 1
        while num > 0:
            num -= odd
            odd += 2
        if num == 0:
            return True
        return False


# 368 - Largest Divisible Subset - MEDIUM
# dynamic programming
# dp[i]: considering the first i numbers,
#        have the largest divisible subset ending with index i
# since we have to give the final solution,
# we need extra 'g[]' to record where does each state transfer from
#
# For the problem of finding the number of solutions,
# it is the most common means to use an extra array
# to record where the state is transferred from.
class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        nums.sort()
        n = len(nums)
        dp, g = [0] * n, [0] * n
        for i in range(n):
            # including number itself, so length start with 1
            length, prev_idx = 1, i
            for j in range(i):
                if nums[i] % nums[j] == 0:
                    # update the max length and where it come from
                    if dp[j] + 1 > length:
                        length = dp[j] + 1
                        prev_idx = j
            # record final 'length' and 'come from'
            dp[i] = length
            g[i] = prev_idx
        max_len = idx = -1
        for i in range(n):
            if dp[i] > max_len:
                max_len = dp[i]
                idx = i
        ans = []
        while len(ans) < max_len:
            ans.append(nums[idx])
            idx = g[idx]
        ans.reverse()
        return ans


# greedy
class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        nums.sort()
        f = [[x] for x in nums]  # answer at nums[i]
        for i in range(len(nums)):
            for j in range(i):
                if nums[i] % nums[j] == 0 and len(f[i]) < len(f[j]) + 1:
                    f[i] = f[j] + [nums[i]]
        return max(f, key=len)


# 372 Super Pow
class Solution:
    def superPow(self, a: int, b: List[int]) -> int:
        return pow(a, int(''.join(map(str, b))), 1337)


class Solution:
    def superPow(self, a: int, b: List[int]) -> int:
        ans = 1
        for digit in b:
            ans = pow(ans, 10, 1337) * pow(a, digit, 1337) % 1337
        return ans


class Solution:
    def superPow(self, a: int, b: List[int]) -> int:
        ans = 1
        for digit in reversed(b):
            ans = ans * pow(a, digit, 1337) % 1337
            a = pow(a, 10, 1337)
        return ans


# 373 - Find K Pairs with Smallest Sums - MEDIUM
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int],
                       k: int) -> List[List[int]]:
        def push(i: int, j: int):
            if i < len(nums1) and j < len(nums2):
                heapq.heappush(queue, [nums1[i] + nums2[j], i, j])

        queue, ans = [], []
        push(0, 0)
        while queue and len(ans) < k:
            _, i, j = heapq.heappop(queue)
            ans.append([nums1[i], nums2[j]])
            push(i, j + 1)
            if j == 0:
                push(i + 1, 0)
        return ans

    def kSmallestPairs(self, nums1: List[int], nums2: List[int],
                       k: int) -> List[List[int]]:
        ans = []
        queue = [(nums1[i] + nums2[0], i, 0)
                 for i in range(min(k, len(nums1)))]
        while queue and len(ans) < k:
            _, i, j = heapq.heappop(queue)
            ans.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heapq.heappush(queue, (nums1[i] + nums2[j + 1], i, j + 1))
        return ans


# 374 - Guess Number Higher or Lower - EASY
# The guess API is already defined for you.
# @param num, your guess
# @return -1 if my number is lower, 1 if my number is higher, otherwise return 0
# def guess(num: int) -> int:


class Solution:
    def guessNumber(self, n: int) -> int:
        left, right, mid = 1, n, 1
        while guess(mid) != 0:
            if guess(mid) > 0:
                left = mid + 1
            else:
                right = mid - 1
            mid = (right + left) // 2
        return mid


def guess(self, n: int) -> int:
    pick = 1  # specify internally
    if n > pick:
        return 1
    elif n < pick:
        return -1
    else:
        return 0


class Solution:
    def guessNumber(self, n: int) -> int:
        left, right = 1, n
        while left < right:
            mid = (left + right) // 2
            if guess(mid) <= 0:
                right = mid  # in [left, mid]
            else:
                left = mid + 1  # in [mid+1, right]

        # at this time left == right
        return left


# 375 - Guess Number Higher or Lower II - MEDIUM
# dp[i][j] means that whatever the number we pick in in [i, j], the minimum money we use to win the game
# dp[1][1] means we have 1 number 1 -> dp[1][1] = 1
# dp[1][2] means we have 2 numbers 1, 2 -> dp[1][2] = 1
# dp[2][3] means we have 2 numbers 2, 3 -> dp[2][3] = 2
# dp[1][3] means we have 3 numbers 1, 2, 3
#   -> dp[2][3] = min(max(0,1+dp[2][3]), max(0,2+dp[1][1],2+dp[3][3]), max(0,3+dp[1][2]))
#                       guess 1                   guess 2                     guess 3
# we can use the downside and leftside value to calcutate dp[i][j]
class Solution:
    def getMoneyAmount(self, n: int) -> int:
        # # intialize
        dp = [[0] * (n + 1) for _ in range(n + 1)]  # dp[n+1][n+1]
        for i in range(n + 1):
            dp[i][i] = 0
        # start with the second column
        for j in range(2, n + 1):
            # from bottom to top
            i = j - 1
            while i >= 1:
                # calculate every split point
                for k in range(i + 1, j):
                    dp[i][j] = min(k + max(dp[i][k - 1], dp[k + 1][j]),
                                   dp[i][j])
                # calculate both sides
                dp[i][j] = min(dp[i][j], i + dp[i + 1][j], j + dp[i][j - 1])
                dp[i][j] = min(dp[i][j], j + dp[i][j - 1])
                i -= 1

        return dp[1][n]

    def getMoneyAmount(self, n: int) -> int:
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n - 1, 0, -1):
            for j in range(i + 1, n + 1):
                dp[i][j] = min(k + max(dp[i][k - 1], dp[k + 1][j])
                               for k in range(i, j))
        return dp[1][n]


# 376 - Wiggle Subsequence - MEDIUM
class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:
        pre, cur, ans = 0, 0, 1  
        for i in range(len(nums) - 1):
            cur = nums[i + 1] - nums[i]
            if cur * pre <= 0 and cur != 0:  
                ans += 1
                pre = cur 
        return ans


# 377 - Combination Sum IV - MEDIUM
class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        dp = [1] + [0] * target
        for i in range(1, target + 1):
            for num in nums:
                if num <= i:
                    dp[i] += dp[i - num]
        return dp[-1]


# 382 - Linked List Random Node - MEDIUM
class Solution:
    def __init__(self, head: Optional[ListNode]):
        self.node = []
        while head:
            self.node.append(head.val)
            head = head.next
        return

    def getRandom(self) -> int:
        return random.choice(self.node)


# reservoir sampling


# 383 - Ransom Note - EASY
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        return not collections.Counter(ransomNote) - collections.Counter(
            magazine)


# 384 - Shuffle an Array - MEDIUM
class Solution:
    def __init__(self, nums: List[int]):
        self.nums = nums[:]
        self.cp = nums[:]

    def reset(self) -> List[int]:
        self.nums[:] = self.cp[:]
        return self.nums

    def shuffle(self) -> List[int]:
        random.shuffle(self.nums)
        return self.nums

    # Fisher-Yates Algorithm
    # the same as built-in function: 'random.shuffle'
    def shuffle(self) -> List[int]:
        n = len(self.nums)
        for i in range(n):
            idx = random.randrange(i, n)
            self.nums[i], self.nums[idx] = self.nums[idx], self.nums[i]
        return self.nums


# Your Solution object will be instantiated and called as such:
# obj = Solution(nums)
# param_1 = obj.reset()
# param_2 = obj.shuffle()


# 390 - Elimination Game - MEDIUM
class Solution(object):
    def lastRemaining(self, n):
        def helper(n: int, isLeft: bool) -> int:
            if (n == 1): return 1
            # if started from left side the odd elements will be removed, the only remaining ones will the the even i.e.
            # [1 2 3 4 5 6 7 8 9] => [2 4 6 8] => 2*[1 2 3 4]
            if isLeft:
                return 2 * helper(n // 2, False)
            # same as left side the odd elements will be removed
            elif (n % 2 == 1):
                return 2 * helper(n // 2, True)
            # even elements will be removed and the only left ones will be [1 2 3 4 5 6] => [1 3 5] => 2*[1 2 3] - 1
            else:
                return 2 * helper(n // 2, True) - 1

        return helper(n, True)

    def lastRemaining(self, n: int) -> int:
        startLeft, ans, step = True, 1, 1
        while n > 1:
            if startLeft or n % 2 == 1:
                ans += step
            startLeft = not startLeft
            step *= 2
            n //= 2
        return ans


# 392 - Is Subsequence - EASY
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = j = 0
        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i += 1
                j += 1
            else:
                j += 1
        return i == len(s)


# 394 - Decode String - MEDIUM
class Solution:
    def decodeString(self, s: str) -> str:
        stack, time, ans = [], 0, ''
        for ch in s:
            if ch == '[':
                stack.append(ans)
                stack.append(time)
                ans = ''
                time = 0
            elif ch == ']':
                pre_num = stack.pop()
                pre_string = stack.pop()
                ans = pre_string + pre_num * ans
            elif ch.isdigit():
                time = time * 10 + int(ch)
            else:
                ans += ch
        return ans


# 397 - Integer Replacement - MEDIUM
# memo
class Solution:
    def __init__(self):
        self.cache = collections.defaultdict(int)

    def integerReplacement(self, n: int) -> int:
        if n == 1:
            return 0
        if n in self.cache:
            return self.cache.get(n)
        if n % 2 == 0:
            self.cache[n] = 1 + self.integerReplacement(n // 2)
        else:
            self.cache[n] = 2 + min(self.integerReplacement(n // 2),
                                    self.integerReplacement(n // 2 + 1))
        return self.cache[n]


class Solution:
    @functools.lru_cache(None)
    def integerReplacement(self, n: int) -> int:
        if n == 1:
            return 0
        if n % 2 == 0:
            return 1 + self.integerReplacement(n // 2)
        return 2 + min(self.integerReplacement(n // 2),
                       self.integerReplacement(n // 2 + 1))


# bfs
class Solution:
    def integerReplacement(self, n: int) -> int:
        dq = collections.deque([n])
        ans = 0
        while dq:
            n = len(dq)
            for _ in range(n):
                number = dq.popleft()
                if number == 1:
                    return ans
                if number % 2 == 0:
                    dq.append(number // 2)
                else:
                    dq.append(number + 1)
                    dq.append(number - 1)
            ans += 1
        return ans
