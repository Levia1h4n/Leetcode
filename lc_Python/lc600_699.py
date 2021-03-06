import itertools, bisect, heapq, collections, math, functools
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# 605 - Can Place Flowers - EASY
class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        f = [0] + flowerbed + [0]
        for i in range(1, len(f) - 1):
            if f[i - 1] == f[i] == f[i + 1] == 0:
                n -= 1
                f[i] = 1
        return n <= 0


# 617 - Merge Two Binary Trees - EASY
class Solution:
    def mergeTrees(self, root1: TreeNode, root2: TreeNode) -> TreeNode:
        if not root1:
            return root2
        if not root2:
            return root1
        root1.val += root2.val
        root1.left = self.mergeTrees(root1.left, root2.left)
        root1.right = self.mergeTrees(root1.right, root2.right)
        return root1

    def mergeTrees(self, root1: TreeNode, root2: TreeNode) -> TreeNode:
        if not root1:
            return root2
        if not root2:
            return root1
        root = TreeNode(root1.val + root2.val)
        root.left = self.mergeTrees(root1.left, root2.left)
        root.right = self.mergeTrees(root1.right, root2.right)
        return root

    def mergeTrees(self, root1: TreeNode, root2: TreeNode) -> TreeNode:
        if root1 and root2:
            root1.val += root2.val
            root1.left = self.mergeTrees(root1.left, root2.left)
            root1.right = self.mergeTrees(root1.right, root2.right)
        return root1 or root2


# 630 - Course Schedule III - HARD
class Solution:
    # O(nlogn) / O(n)
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        courses.sort(key=lambda c: c[1])
        pq = []
        t = 0
        for d, ddl in courses:
            t += d
            if t > ddl:
                t += heapq.heappushpop(pq, -d)
                # t -= -heapq.heappushpop(pq, -d)
            else:
                heapq.heappush(pq, -d)

            # or
            # if t + d <= ddl:
            #     t += d
            #     heapq.heappush(pq, -d)
            # elif pq and -pq[0] > d:
            #     # t += heapq.heappushpop(pq, -d) + d
            #     t -= -pq[0] - d
            #     heapq.heappop(pq)
            #     heapq.heappush(pq, -d)
        return len(pq)

    def scheduleCourse(self, courses: List[List[int]]) -> int:
        pq = []
        t = 0
        for d, ddl in sorted(courses, key=lambda x: x[1]):
            if t + d > ddl and pq and -pq[0] > d:
                t += heapq.heappop(pq)
            if t + d <= ddl:
                heapq.heappush(pq, -d)
                t += d
        return len(pq)


# 637 - Average of Levels in Binary Tree - EASY
class Solution:
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        ans = []
        q = [root]
        while q:
            t = summ = 0
            new = []
            for _ in range(len(q)):
                n = q.pop()
                if n.left:
                    new.append(n.left)
                if n.right:
                    new.append(n.right)
                t += 1
                summ += n.val
            ans.append(summ / t)
            q = new
        return ans


# 648 - Replace Words - MEDIUM
class Solution:
    # O(sdw + dlogd) / O(s + logd), w = len(each word in d)
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        sentence = sentence.split()
        dictionary.sort()  # ori: catt, cat -> sorted: cat, catt
        for i, s in enumerate(sentence):
            for d in dictionary:
                if s.startswith(d):
                    sentence[i] = d
                    break
        return " ".join(sentence)

    # O(dw + sw) / O(dw + s), w = len(each word in s)
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        trie = dict()
        for w in dictionary:
            r = trie
            for c in w:
                if c not in r:
                    r[c] = {}
                r = r[c]
            r["#"] = 3  # ending flag
        sentence = sentence.split()
        for i, w in enumerate(sentence):
            r = trie
            for j, c in enumerate(w):
                if "#" in r:
                    sentence[i] = w[:j]
                    break
                if c not in r:
                    break
                r = r[c]
        return " ".join(sentence)


# 653 - Two Sum IV - Input is a BST - EASY
class Solution:
    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        if not root:
            return False
        bfs, s = [root], set()
        for i in bfs:
            if k - i.val in s:
                return True
            s.add(i.val)
            if i.left:
                bfs.append(i.left)
            if i.right:
                bfs.append(i.right)
        return False


# 661 - Image Smoother - EASY
class Solution:
    def imageSmoother(self, img: List[List[int]]) -> List[List[int]]:
        m = len(img)
        n = len(img[0])
        p = [[0] * (n + 1) for _ in range(m + 1)]
        a = [[0] * n for _ in range(m)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                p[i][j] = (
                    p[i - 1][j] + p[i][j - 1] - p[i - 1][j - 1] + img[i - 1][j - 1]
                )
        for i in range(m):
            for j in range(n):
                x1 = max(i - 1, 0)
                y1 = max(j - 1, 0)
                x2 = min(i + 2, m)
                y2 = min(j + 2, n)
                a[i][j] = (p[x2][y2] - p[x1][y2] - p[x2][y1] + p[x1][y1]) // (
                    (x2 - x1) * (y2 - y1)
                )
        return a

    def imageSmoother(self, img: List[List[int]]) -> List[List[int]]:
        m = len(img)
        n = len(img[0])
        ans = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                t, c = 0, 0
                for x in range(max(i - 1, 0), min(i + 2, m)):
                    for y in range(max(j - 1, 0), min(j + 2, n)):
                        t += img[x][y]
                        c += 1
                ans[i][j] = t // c
        return ans


# 673 - Number of Longest Increasing Subsequence - MEDIUM
class Solution:
    # O(n^2)
    def findNumberOfLIS(self, nums: List[int]) -> int:
        dp = [1] * len(nums)
        cnt = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        cnt[i] = cnt[j]
                    elif dp[j] + 1 == dp[i]:
                        cnt[i] += cnt[j]
        ans = 0
        for i in range(len(nums)):
            if dp[i] == max(dp):
                ans += cnt[i]
        return ans

    # O(nlogn)
    def findNumberOfLIS(self, nums: List[int]) -> int:
        dp = []
        cnt = collections.defaultdict(list)
        for num in nums:
            idx = bisect.bisect_left(dp, num)
            if idx == len(dp):
                dp.append(num)
            else:
                dp[idx] = num
            total = 0
            for count, last in cnt[idx]:
                if last < num:
                    total += count
            cnt[idx + 1].append((max(1, total), num))
        return sum([count for count, _ in cnt[len(dp)]])


# 670 - Maximum Swap - MEDIUM
# Greedy, O(n)
# find the last occurrence of each number (guarantee that the rightmost number)
# enumerate each number from left to right,
# swap the number when a larger number is found
class Solution:
    def maximumSwap(self, num: int) -> int:
        s = list(str(num))
        later = {int(x): i for i, x in enumerate(s)}
        for i, x in enumerate(s):
            for d in range(9, int(x), -1):
                if later.get(d, -1) > i:
                    s[i], s[later[d]] = s[later[d]], s[i]
                    return "".join(s)
        return num


# 676 - Implement Magic Dictionary - MEDIUM
class MagicDictionary:
    def __init__(self):
        self.w = list()

    def buildDict(self, dictionary: List[str]) -> None:
        self.w = dictionary

    def search(self, searchWord: str) -> bool:
        for w in self.w:
            if len(w) != len(searchWord):
                continue
            diff = 0
            for a, b in zip(w, searchWord):
                if a != b:
                    diff += 1
                if diff > 1:
                    break
            if diff == 1:
                return True
        return False


class MagicDictionary:
    def __init__(self):
        self.dic = {}

    def buildDict(self, dictionary: List[str]) -> None:
        for i in dictionary:
            self.dic[len(i)] = self.dic.get(len(i), []) + [i]

    def search(self, searchWord: str) -> bool:
        for candi in self.dic.get(len(searchWord), []):
            diff = 0
            for j in range(len(searchWord)):
                if candi[j] != searchWord[j]:
                    diff += 1
                if diff > 1:
                    break
            if diff == 1:
                return True
        return False


class MagicDictionary:
    def __init__(self):
        self.dic = {}

    def buildDict(self, dictionary: List[str]) -> None:
        for d in dictionary:
            self.dic.setdefault(len(d), []).append(d)

    def search(self, searchWord: str) -> bool:
        l = len(searchWord)
        for candidate in self.dic.get(l, []):
            isDifferent = False
            for idx in range(l):
                if candidate[idx] != searchWord[idx]:
                    if isDifferent:
                        break
                    else:
                        isDifferent = True
            else:
                if isDifferent:
                    return True
        return False


# 677 - Map Sum Pairs - MEDIUM
class MapSum:
    def __init__(self):
        self.d = {}

    def insert(self, key: str, val: int) -> None:
        self.d[key] = val

    def sum(self, prefix: str) -> int:
        return sum(self.d[i] for i in self.d if i.startswith(prefix))


# 678 - Valid Parenthesis String - MEDIUM
class Solution:
    # stack[index], be careful of '*(': '*' is at the left of '('
    def checkValidString(self, s: str) -> bool:
        left, star = [], []
        for i, ch in enumerate(list(s)):
            if ch == ")":
                if not left:
                    if not star:
                        return False
                    else:
                        star.pop()
                else:
                    left.pop()
            elif ch == "(":
                left.append(i)
            else:
                star.append(i)
        if len(star) < len(left):
            return False
        for i in range(len(left)):
            if left[-i - 1] > star[-i - 1]:
                return False
        return True

    # check two directions
    def checkValidString(self, s: str) -> bool:
        # left to right
        stack = []
        for x in s:
            if x == "(" or x == "*":
                stack.append(x)
            else:
                if len(stack) > 0:
                    stack.pop()
                else:
                    return False
        # right to left
        stack = []
        for x in s[::-1]:
            if x == ")" or x == "*":
                stack.append(x)
            else:
                if len(stack) > 0:
                    stack.pop()
                else:
                    return False
        return True

    # greedy, possible minimum and maximum values of '('
    def checkValidString(self, s: str) -> bool:
        cmin = cmax = 0
        for i in s:
            if i == "(":
                cmax += 1
                cmin += 1
            if i == ")":
                cmax -= 1
                cmin = max(cmin - 1, 0)
            if i == "*":
                cmax += 1
                cmin = max(cmin - 1, 0)
            if cmax < 0:
                return False
        return cmin == 0


# 680 - Valid Palindrome II - EASY
class Solution:
    def validPalindrome(self, s: str) -> bool:
        i, j = 0, len(s) - 1
        while i < j:
            if s[i] != s[j]:
                deleteJ = s[i:j]
                deleteI = s[i + 1 : j + 1]
                return deleteI == deleteI[::-1] or deleteJ == deleteJ[::-1]
            i += 1
            j -= 1
        return True

    def validPalindrome(self, s):
        i = 0
        while i < len(s) / 2 and s[i] == s[-(i + 1)]:
            i += 1
        s = s[i : len(s) - i]
        return s[1:] == s[1:][::-1] or s[:-1] == s[:-1][::-1]


# 682 - Baseball Game - EASY
class Solution:
    def calPoints(self, ops: List[str]) -> int:
        s = []
        for ch in ops:
            if ch == "D":
                s.append(2 * s[-1])
            elif ch == "C":
                s.pop()
            elif ch == "+":
                s.append(s[-1] + s[-2])
            else:
                s.append(int(ch))
        return sum(s)


# 686 - Repeated String Match - MEDIUM
class Solution:
    def repeatedStringMatch(self, a: str, b: str) -> int:
        i, cp_a = 1, a
        max_l = len(a) * 2 + len(b)
        while len(a) < max_l:
            if b in a:
                return i
            else:
                i += 1
                a += cp_a
        return -1


# 687 - Longest Univalue Path - MEDIUM
class Solution:
    def longestUnivaluePath(self, root: TreeNode) -> int:
        def postorder(root: TreeNode):  # return root.val and the longest path
            if not root:
                return (-1001, 0)
            left, ll = postorder(root.left)
            right, rl = postorder(root.right)
            l = 0
            if root.val == left == right:
                # two subtree may consist a longer path
                self.ans = max(self.ans, ll + rl + 2)
                l += max(ll, rl) + 1
            elif left == root.val:
                l += ll + 1
            elif right == root.val:
                l += rl + 1
            self.ans = max(self.ans, l)
            return (root.val, l)

        self.ans = 0
        postorder(root)
        return self.ans

    def longestUnivaluePath(self, root: TreeNode) -> int:
        def postorder(node: TreeNode, parent_val: int) -> int:
            if not node:
                return 0
            left = postorder(node.left, node.val)
            right = postorder(node.right, node.val)
            self.longest = max(self.longest, left + right)
            return 1 + max(left, right) if node.val == parent_val else 0

        self.longest = 0
        postorder(root, None)
        return self.longest


# 688 - Knight Probability in Chessboard - MEDIUM
class Solution:
    def knightProbability(self, n: int, k: int, row: int, column: int) -> float:
        dp = [[[0] * n for _ in range(n)] for _ in range(k + 1)]
        for step in range(k + 1):
            for i in range(n):
                for j in range(n):
                    if step == 0:
                        dp[step][i][j] = 1
                    else:
                        for di, dj in (
                            (-2, -1),
                            (-2, 1),
                            (2, -1),
                            (2, 1),
                            (-1, -2),
                            (-1, 2),
                            (1, -2),
                            (1, 2),
                        ):
                            ni, nj = i + di, j + dj
                            if 0 <= ni < n and 0 <= nj < n:
                                dp[step][i][j] += dp[step - 1][ni][nj] / 8
        return dp[k][row][column]

    def knightProbability(self, N, K, r, c):
        memo = {}

        def dfs(i, j, p, k):
            if 0 <= i < N and 0 <= j < N and k < K:
                sm = 0
                for x, y in (
                    (-1, -2),
                    (-2, -1),
                    (-2, 1),
                    (-1, 2),
                    (1, 2),
                    (2, 1),
                    (2, -1),
                    (1, -2),
                ):
                    if (i + x, j + y, k) not in memo:
                        memo[(i + x, j + y, k)] = dfs(i + x, j + y, p / 8, k + 1)
                    sm += memo[(i + x, j + y, k)]
                return sm
            else:
                return 0 <= i < N and 0 <= j < N and p or 0

        return dfs(r, c, 1, 0)


# 689 - Maximum Sum of 3 Non-Overlapping Subarrays - HARD
class Solution:
    def maxSumOfThreeSubarrays(self, nums: List[int], k: int) -> List[int]:
        # Best single, double, and triple sequence found so far
        bestSeq = 0
        bestTwoSeq = [0, k]
        bestThreeSeq = [0, k, k * 2]

        # Sums of each window
        seqSum = sum(nums[0:k])
        seqTwoSum = sum(nums[k : k * 2])
        seqThreeSum = sum(nums[k * 2 : k * 3])

        # Sums of combined best windows
        bestSeqSum = seqSum
        bestTwoSum = seqSum + seqTwoSum
        bestThreeSum = seqSum + seqTwoSum + seqThreeSum

        # Current window positions
        seqIndex = 1
        twoSeqIndex = k + 1
        threeSeqIndex = k * 2 + 1
        while threeSeqIndex <= len(nums) - k:
            # Update the three sliding windows
            seqSum = seqSum - nums[seqIndex - 1] + nums[seqIndex + k - 1]
            seqTwoSum = seqTwoSum - nums[twoSeqIndex - 1] + nums[twoSeqIndex + k - 1]
            seqThreeSum = (
                seqThreeSum - nums[threeSeqIndex - 1] + nums[threeSeqIndex + k - 1]
            )

            # Update best single window
            if seqSum > bestSeqSum:
                bestSeq = seqIndex
                bestSeqSum = seqSum

            # Update best two windows
            if seqTwoSum + bestSeqSum > bestTwoSum:
                bestTwoSeq = [bestSeq, twoSeqIndex]
                bestTwoSum = seqTwoSum + bestSeqSum

            # Update best three windows
            if seqThreeSum + bestTwoSum > bestThreeSum:
                bestThreeSeq = bestTwoSeq + [threeSeqIndex]
                bestThreeSum = seqThreeSum + bestTwoSum

            # Update the current positions
            seqIndex += 1
            twoSeqIndex += 1
            threeSeqIndex += 1

        return bestThreeSeq


# 693 - Binary Number with Alternating Bits - EASY
class Solution:
    def hasAlternatingBits(self, n: int) -> bool:
        p = n & 1
        n >>= 1
        while n:
            if n & 1 == p:
                return False
            p = 1 - p
            n >>= 1
        return True

    def hasAlternatingBits(self, n: int) -> bool:
        a = n ^ (n >> 1)
        return a & (a + 1) == 0


# 695 - Max Area of Island - MEDIUM
class Solution:
    # dfs
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        self.area, ans, m, n = 0, 0, len(grid), len(grid[0])

        def dfs(x: int, y: int):
            self.area += 1
            grid[x][y] = -1  # visited
            for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if 0 <= i < m and 0 <= j < n and grid[i][j] == 1:
                    dfs(i, j)
            return

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:  # search
                    dfs(i, j)
                    ans = max(ans, self.area)
                    self.area = 0
        return ans

    # dfs
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        def dfs(i: int, j: int) -> int:
            if 0 <= i < m and 0 <= j < n and grid[i][j]:
                grid[i][j] = 0
                return 1 + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i + 1, j) + dfs(i, j - 1)
            return 0

        areas = [dfs(i, j) for i in range(m) for j in range(n) if grid[i][j]]
        return max(areas) if areas else 0


# 696 - Count Binary Substrings - EASY
class Solution:
    def countBinarySubstrings(self, s: str) -> int:
        ans, prev, cur = 0, 0, 1
        for i in range(1, len(s)):
            if s[i] != s[i - 1]:
                ans += min(prev, cur)
                prev = cur
                cur = 1
            else:
                cur += 1
        ans += min(prev, cur)
        return ans


# 699 - Falling Squares - HARD
class Solution:
    # O(n ** 2) / O(1)
    def fallingSquares(self, positions: List[List[int]]) -> List[int]:
        n = len(positions)
        heights = [0] * n
        for i, (l, sz) in enumerate(positions):
            r = l + sz - 1
            heights[i] = sz
            for j in range(i):
                ll, rr = positions[j][0], positions[j][0] + positions[j][1] - 1
                if r >= ll and l <= rr:
                    heights[i] = max(heights[i], heights[j] + sz)
        for i in range(1, n):
            heights[i] = max(heights[i], heights[i - 1])
        return heights

    # segment tree: TODO
