from typing import List, Optional
import collections, functools, copy, random


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# 102 - Binary Tree Level Order Traversal - MEDIUM
# bfs: breadth-first search
class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        ans, values = [], []
        nodeStack = collections.deque()
        if root:
            nodeStack.append(root)
        while nodeStack:
            for _ in list(nodeStack):
                node = nodeStack.popleft()
                if node.left:
                    nodeStack.append(node.left)
                if node.right:
                    nodeStack.append(node.right)
                values.append(node.val)
            ans.append(values)
            values = []
        return ans


# dfs: depth-first search
class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        ans = []

        def dfs(root: TreeNode, level: int):
            if not root:
                return
            if level == len(ans):
                ans.append([])
            ans[level].append(root.val)
            dfs(root.left, level + 1)
            dfs(root.right, level + 1)
            return

        dfs(root, 0)
        return ans


# 104 - Maximum Depth of Binary Tree - EASY
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1


# 121 - Best Time to Buy and Sell Stock - EASY
# Dynamic Programming
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        hisLowPrice, ans = prices[0], 0
        for price in prices:
            ans = max(ans, price - hisLowPrice)
            hisLowPrice = min(hisLowPrice, price)
        return ans


# 125 - Valid Palindrome - EASY
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        s = "".join([
            ch for ch in s if (97 <= ord(ch) and ord(ch) <= 122) or (
                48 <= ord(ch) and ord(ch) <= 57)
        ])
        # s.isalnum(): alphabet or numeric
        # s = "".join(ch.lower() for ch in s if ch.isalnum())
        return s == s[::-1]


# 128 - Longest Consecutive Sequence - MEDIUM
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        nums = set(nums)
        longest = 0
        for num in nums:
            if num - 1 not in nums:
                curNum = num
                curLen = 1
                while curNum + 1 in nums:
                    curNum += 1
                    curLen += 1
                '''
                'curLen' can be optimized
                nextOne = num + 1
                while nextOne in nums:
                    nextOne += 1
                longest = max(longest, nextOne - num)
                '''
                longest = max(longest, curLen)
        return longest


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        nums, maxlen = set(nums), 0
        while nums:
            num = nums.pop()
            l, r = num - 1, num + 1
            while l in nums:
                nums.remove(l)
                l -= 1
            while r in nums:
                nums.remove(r)
                r += 1
            l += 1
            r -= 1
            maxlen = max(maxlen, r - l + 1)
        return maxlen


# 129 - Sum Root to Leaf Numbers - MEDIUM
# dfs
class Solution:
    def sumNumbers(self, root: TreeNode) -> int:
        def dfs(root: TreeNode, pre: int) -> int:
            if not root:
                return 0
            cur = pre * 10 + root.val
            if not root.left and not root.right:
                return cur
            return dfs(root.left, cur) + dfs(root.right, cur)

        return dfs(root, 0)


# bfs
class Solution:
    def sumNumbers(self, root: TreeNode) -> int:
        total = 0
        nodes = collections.deque([root])
        # (vals) can be optimized spatially. before each node put into deque, change the value of node
        vals = collections.deque([root.val])
        while nodes:
            node = nodes.popleft()
            val = vals.popleft()
            if not node.left and not node.right:
                total += val
            else:
                if node.left:
                    nodes.append(node.left)
                    vals.append(node.left.val + val * 10)
                if node.right:
                    nodes.append(node.right)
                    vals.append(node.right.val + val * 10)

        return total


# 130 - Surrounded Regions - MEDIUM
# search from edge
# dfs
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        row, col = len(board), len(board[0])

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def dfs(i: int, j: int):
            if 0 <= i < row and 0 <= j < col and board[i][j] == "O":
                board[i][j] = "*"
                for x, y in directions:
                    dfs(i + x, j + y)
            return

        for i in range(row):
            dfs(i, 0)
            dfs(i, col - 1)
        for j in range(col):
            dfs(0, j)
            dfs(row - 1, j)
        for i in range(row):
            for j in range(col):
                board[i][j] = "X" if board[i][j] != "*" else "O"
        return


# bfs
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        dq = collections.deque([])
        row, col = len(board), len(board[0])
        for r in range(row):
            for c in range(col):
                if (r in [0, row - 1]
                        or c in [0, col - 1]) and board[r][c] == "O":
                    dq.append((r, c))
        while dq:
            r, c = dq.popleft()
            if 0 <= r < row and 0 <= c < col and board[r][c] == "O":
                board[r][c] = "*"
                dq.extend([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)])

        for i in range(row):
            for j in range(col):
                board[i][j] = "X" if board[i][j] != "*" else "O"
        return


# 134 - Gas Station - MEDIUM
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total, station, minTotal = 0, 0, float("inf")
        for i in range(len(gas)):
            total += gas[i] - cost[i]
            if total < minTotal:
                station = i
                minTotal = total
        return (station + 1) % len(gas) if total >= 0 else -1


# 136 - Single Number - EASY
# XOR operation
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        ans = 0
        for i in nums:
            ans ^= i
        return ans


# lambda arguments: expression
# reduce(func, seq)
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        # return functools.reduce(operator.xor, nums)
        return functools.reduce(lambda x, y: x ^ y, nums)


# 137 - Single Number II - MEDIUM
# sort, jump 3 element
# use HashMap also works
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        cnt = collections.Counter(nums)
        ans = [num for num, times in cnt.items() if times == 1]
        return ans[0]


class Solution:  # 没看懂
    def singleNumber(self, nums: List[int]) -> int:
        b1, b2 = 0, 0  # 出现一次的位，和两次的位
        for n in nums:
            # 既不在出现一次的b1，也不在出现两次的b2里面，我们就记录下来，出现了一次，再次出现则会抵消
            b1 = (b1 ^ n) & ~b2
            # 既不在出现两次的b2里面，也不再出现一次的b1里面(不止一次了)，记录出现两次，第三次则会抵消
            b2 = (b2 ^ n) & ~b1
        return b1


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)


# 138 - Copy List with Random Pointer - MEDIUM
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        return copy.deepcopy(head)


class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        if not head:
            return None
        dic = {}
        headCP = head
        # save node value
        while head:
            valHead = Node(head.val)
            dic[head] = valHead
            head = head.next
        head = headCP
        tmp = dic[head]
        ans = tmp
        # process random pointer
        while head:
            if head.next:
                tmp.next = dic[head.next]
            if head.random:
                tmp.random = dic[head.random]
            head = head.next
            tmp = tmp.next
        return ans


# 146 - LRU Cache - MEDIUM
class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.dic = {}
        self.seq = collections.deque()

    def get(self, key: int) -> int:
        value = self.dic.get(key, -1)
        if value != -1:
            self.seq.remove(key)
            self.seq.append(key)
        return value

    def put(self, key: int, value: int) -> None:
        # have the same key
        if key in self.dic:
            self.dic[key] = value
            self.seq.remove(key)
            self.seq.append(key)
            return
        # whether cache reach to the capacity
        if len(self.dic) == self.cap:
            delete = self.seq.popleft()
            self.dic.pop(delete)
        # insert
        self.dic[key] = value
        self.seq.append(key)
        return


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        # del self.cache[key]
        # # del is faster, pop() or popitem() used to get the return value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# 162 - Find Peak Element - MEDIUM
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return 0
        if nums[0] > nums[1]:
            return 0
        if len(nums) == 2:
            return 1
        for i in range(1, len(nums) - 1):
            if nums[i - 1] < nums[i] and nums[i] > nums[i + 1]:
                return i
        return len(nums) - 1


# climbing to the greater side
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        idx = random.randint(0, len(nums) - 1)

        # helper function: help to handle boundary situations
        def getValue(i: int) -> int:
            if i == -1 or i == len(nums):
                return float("-inf")
            return nums[i]

        while not (getValue(idx - 1) < getValue(idx)
                   and getValue(idx) > getValue(idx + 1)):
            if getValue(idx) < getValue(idx + 1):
                idx += 1
            else:
                idx -= 1
        return idx


# 167 - Two Sum II - Input Array Is Sorted - EASY
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dic = {}
        for i in range(len(nums)):
            if nums[i] in dic:
                return [dic[nums[i]] + 1, i + 1]
            else:
                dic[target - nums[i]] = i
        return [-1, -1]


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left, right = 0, len(numbers) - 1
        while left < right:
            summ = numbers[left] + numbers[right]
            if summ < target:
                left += 1
            elif summ > target:
                right -= 1
            else:
                return [left + 1, right + 1]
        return [-1, -1]


# 173 - Binary Search Tree Iterator - MEDIUM
# save all node.val by inorder traversal
class BSTIterator:
    def __init__(self, root: Optional[TreeNode]):
        self.stack = collections.deque()
        self.inorder(root)

    def next(self) -> int:
        return self.stack.popleft()

    def hasNext(self) -> bool:
        return len(self.stack) > 0

    def inorder(self, root: TreeNode) -> None:
        if not root:
            return
        self.inorder(root.left)
        self.stack.append(root.val)
        self.inorder(root.right)
        return


# iterate. save all left nodes while pop each node
class BSTIterator:
    def __init__(self, root: TreeNode):
        self.stack = []
        while root:
            self.stack.append(root)
            root = root.left

    def next(self):
        cur = self.stack.pop()
        node = cur.right
        while node:
            self.stack.append(node)
            node = node.left
        return cur.val

    def hasNext(self) -> bool:
        return len(self.stack) > 0


# Abstract the putting into stack operation into a function
class BSTIterator:
    def __init__(self, root: TreeNode):
        self.stack = []
        self.pushAllLeftNodes(root)

    def next(self):
        cur = self.stack.pop()
        node = cur.right
        self.pushAllLeftNodes(node)
        return cur.val

    def hasNext(self) -> bool:
        return len(self.stack) > 0

    def pushAllLeftNodes(self, root: TreeNode) -> None:
        while root:
            self.stack.append(root)
            root = root.left
        return


# 189 - Rotate Array - MEDIUM
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        k %= len(nums)
        '''
        Input: [1], 0
        Wrong: nums[:k], nums[k:] = nums[-k:], nums[:-k]
        Assignment Visualization: [], [1] = [1], []
        Conclusion: assignment from left to right
        '''
        nums[k:], nums[:k] = nums[:-k], nums[-k:]
        # nums[:] = nums[-k:] + nums[:-k]
        return


# 198 - House Robber - MEDIUM
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) < 3:
            return max(nums)
        dp = [0] * len(nums)
        dp[0], dp[1] = nums[0], max(nums[0], nums[1])
        for i in range(2, len(nums)):
            dp[i] = max(dp[i - 2] + nums[i], dp[i - 1])
        return dp[-1]


class Solution:
    def rob(self, nums: List[int]) -> int:
        dp1, dp2 = 0, 0
        for i in range(len(nums)):
            dp1, dp2 = dp2, max(dp1 + nums[i], dp2)
        return dp2


# 199 - Binary Tree Right Side View - MEDIUM
# dfs postorder
class Solution:
    def rightSideView(self, root: TreeNode) -> List[int]:
        ans = []

        def postorder(root: TreeNode, level: int):
            if root == None:
                return
            if level == len(ans):
                ans.append(root.val)
            level += 1
            postorder(root.right, level)
            postorder(root.left, level)
            return

        postorder(root, 0)
        return ans


# bfs
# use dequeue to save every nodes in each level
# FIFO
class Solution:
    def rightSideView(self, root: TreeNode) -> List[int]:
        dq = collections.deque()
        if root:
            dq.append(root)
        ans = []
        while dq:
            # queue is not empty
            ans.append(dq[-1].val)
            for _ in range(len(dq)):
                node = dq.popleft()
                if node.left:
                    dq.append(node.left)
                if node.right:
                    dq.append(node.right)
        return ans


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        # bfs
        dq = collections.deque()
        if root:
            dq.append(root)
        ans = []
        level = 0
        while dq:
            # process each layer
            for _ in range(len(dq)):
                node = dq.pop()
                # not have node be seen in this layer, add rightmost node first
                if len(ans) == level:
                    ans.append(node.val)
                # right side view, add right node first
                if node.right:
                    dq.appendleft(node.right)
                if node.left:
                    dq.appendleft(node.left)
            level += 1
        return ans


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        # bfs
        dq = collections.deque()
        if root:
            dq.append(root)
        ans, level = [], 0
        while dq:
            # process each layer
            for _ in range(len(dq)):
                node = dq.popleft()
                # add from left, so need to update
                if len(ans) == level:
                    ans.append(node.val)
                else:
                    ans[level] = node.val
                if node.left:
                    dq.append(node.left)
                if node.right:
                    dq.append(node.right)
            level += 1
        return ans