from operator import imatmul
from typing import List
import collections, itertools


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# 700 - Search in a Binary Search Tree - EASY
class Solution:
    def searchBST(self, root: TreeNode, val: int) -> TreeNode:
        while root:
            if root.val < val:
                root = root.right
            elif root.val > val:
                root = root.left
            else:
                return root
        return None


# 704 - Binary Search - EASY
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (right + left) // 2
            if nums[mid] > target:
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                return mid
        return -1


# 709 -To Lower Case - EASY
class Solution:
    def toLowerCase(self, s: str) -> str:
        '''
        upper, lower exchange: asc ^= 32;
        upper, lower to lower: asc |= 32;
        lower, upper to upper: asc &= -33
        '''
        return "".join(
            chr(asc | 32) if 65 <= (asc := ord(ch)) <= 90 else ch for ch in s)
        return s.lower()


# 721 - Accounts Merge - MEDIUM
class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        name = set()
        dic = {}

        def ifexist(account: List[str]) -> bool:
            for acc in account[1:]:
                for i, person in enumerate(dic[account[0]]):
                    for p in person:
                        if acc == p:
                            # the same person
                            dic[account[0]][i] = dic[account[0]][i].union(
                                set(account[1:]))
                            return True
            return False

        for account in accounts:
            if account[0] not in name:
                dic[account[0]] = [set(account[1:])]
                name.add(account[0])
            else:
                ex = ifexist(account)
                if not ex:
                    dic[account[0]].append(set(account[1:]))
        ans = []
        name = list(name)
        name.sort()
        for samename in name:
            for person in dic[samename]:
                tmp = [samename]
                tmp.extend(list(person))
                ans.append(tmp)
        return ans


# UnionFind
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def union(self, index1: int, index2: int):
        self.parent[self.find(index2)] = self.find(index1)

    def find(self, index: int) -> int:
        if self.parent[index] != index:
            self.parent[index] = self.find(self.parent[index])
        return self.parent[index]


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        emailToIndex = dict()
        emailToName = dict()

        for account in accounts:
            name = account[0]
            for email in account[1:]:
                if email not in emailToIndex:
                    emailToIndex[email] = len(emailToIndex)
                    emailToName[email] = name

        uf = UnionFind(len(emailToIndex))
        for account in accounts:
            firstIndex = emailToIndex[account[1]]
            for email in account[2:]:
                uf.union(firstIndex, emailToIndex[email])

        indexToEmails = collections.defaultdict(list)
        for email, index in emailToIndex.items():
            index = uf.find(index)
            indexToEmails[index].append(email)

        ans = list()
        for emails in indexToEmails.values():
            ans.append([emailToName[emails[0]]] + sorted(emails))
        return ans


# 733 - Flood Fill - EASY
class Solution:
    # bfs
    def floodFill(self, image: List[List[int]], sr: int, sc: int,
                  newColor: int) -> List[List[int]]:
        if image[sr][sc] == newColor:
            return image
        position, originalColor = [(sr, sc)], image[sr][sc]
        while position:
            pos = position.pop()
            image[pos[0]][pos[1]] = newColor
            for m in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if 0 <= pos[0] + m[0] < len(
                        image) and 0 <= pos[1] + m[1] < len(
                            image[0]) and image[pos[0] +
                                                m[0]][pos[1] +
                                                      m[1]] == originalColor:
                    position.append((pos[0] + m[0], pos[1] + m[1]))
        return image

    # dfs
    def floodFill(self, image: List[List[int]], sr: int, sc: int,
                  newColor: int) -> List[List[int]]:
        if image[sr][sc] == newColor:
            return image
        originalColor = image[sr][sc]

        def dfs(row: int, col: int):
            image[row][col] = newColor
            for m in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if 0 <= row + m[0] < len(image) and 0 <= col + m[1] < len(
                        image[0]) and image[row + m[0]][col +
                                                        m[1]] == originalColor:
                    dfs(row + m[0], col + m[1])
            return

        dfs(sr, sc)
        return image

    # recursive
    def floodFill(self, image: List[List[int]], sr: int, sc: int,
                  newColor: int) -> List[List[int]]:
        if image[sr][sc] == newColor:
            return image
        originalColor = image[sr][sc]
        image[sr][sc] = newColor
        for x, y in [(sr + 1, sc), (sr - 1, sc), (sr, sc + 1), (sr, sc - 1)]:
            if 0 <= x < len(image) and 0 <= y < len(
                    image[0]) and image[x][y] == originalColor:
                self.floodFill(image, x, y, newColor)
        return image


# 740 - Delete and Earn - MEDIUM
class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:
        maxVal = max(nums)
        v = [0] * (maxVal + 1)
        for val in nums:
            v[val] += val
        pre, cur = 0, 0  # 198 - House Robber
        for i in range(1, len(v)):
            pre, cur = cur, max(pre + v[i], cur)
        return cur


# 746 - Min Cost Climbing Stairs - EASY
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        dp = [0] * len(cost)
        dp[0], dp[1] = cost[0], cost[1]
        for i in range(2, len(cost)):
            dp[i] = min(dp[i - 2], dp[i - 1]) + cost[i]
        return min(dp[-2], dp[-1])


# 747


# 748 - Shortest Completing Word - EASY
class Solution:
    def shortestCompletingWord(self, licensePlate: str,
                               words: List[str]) -> str:
        licensePlate = [
            x for x in licensePlate.lower() if ord('a') <= ord(x) <= ord('z')
        ]
        s, cnt = set(licensePlate), collections.Counter(licensePlate)
        for word in sorted(words, key=lambda word: len(word)):
            word = [x for x in word.lower() if ord('a') <= ord(x) <= ord('z')]
            '''
            Counter(word) - cnt: means that cnt(word) strictly larger than cnt
            not including the case: cnt(word) == cnt
            '''
            if set(word).intersection(
                    s) == s and not cnt - collections.Counter(word):
                return "".join(word)
        return ""

    # not use set, counter all character in each word, a little bit slow
    def shortestCompletingWord(self, licensePlate: str,
                               words: List[str]) -> str:
        pc = collections.Counter(filter(str.isalpha, licensePlate.lower()))
        return min([w for w in words if collections.Counter(w) & pc == pc],
                   key=len)


# 749

# 750


# 784 - Letter Case Permutation - MEDIUM
class Solution:
    def letterCasePermutation(self, s: str) -> List[str]:
        ans = ['']
        for ch in s:
            if ch.isalpha():
                ans = [i + j for i in ans for j in [ch.upper(), ch.lower()]]
            else:
                ans = [i + ch for i in ans]
        return ans

        # ans = ['']
        # for c in s.lower():
        #     ans = [a + c
        #            for a in ans] + ([a + c.upper()
        #                              for a in ans] if c.isalpha() else [])
        # return ans

        ## L = ['a', 'A'], '1', ['b', 'B'], '2']
        ## itertools.product(L) --> only 1 parameter [['a', 'A'], '1', ['b', 'B'], '2']
        ## itertools.product(*L) --> 4 parameter ['a', 'A'], '1', ['b', 'B'], '2'
        # L = [set([i.lower(), i.upper()]) for i in s]
        # return map(''.join, itertools.product(*L))

    def letterCasePermutation(self, s: str) -> List[str]:
        def backtrack(sub: str, i: int):
            if len(sub) == len(s):
                ans.append(sub)
            else:
                if s[i].isalpha():
                    # chr(ord(s[i])^(1<<5))
                    backtrack(sub + s[i].swapcase(), i + 1)
                    # backtrack(sub + s[i].lower(), i + 1)
                backtrack(sub + s[i], i + 1)
                # backtrack(sub + s[i].upper(), i + 1)

        ans = []
        backtrack("", 0)
        return ans


# 785
# 786 - K-th Smallest Prime Fraction - HARD
class Solution:
    def kthSmallestPrimeFraction(self, arr: List[int], k: int) -> List[int]:
        div = []
        for i in range(len(arr) - 1):
            for j in range(i + 1, len(arr)):
                div.append((arr[i], arr[j]))
        div.sort(key=lambda x: x[0] / x[1])
        return div[k - 1]

    def kthSmallestPrimeFraction(self, arr: List[int], k: int) -> List[int]:
        left, right = 0, 1
        while True:
            mid = (left + right) / 2
            i, count, x, y = -1, 0, 0, 1
            for j in range(1, len(arr)):
                while arr[i + 1] / arr[j] < mid:
                    i += 1
                    # a/b > c/d => a*d > b*c
                    # update the max fraction
                    if arr[i] * y > arr[j] * x:
                        x, y = arr[i], arr[j]
                count += i + 1

            if count > k:
                right = mid
            if count < k:
                left = mid
            else:
                return [x, y]


# 787

# 788

# 789

# 790


# 791 - Custom Sort String - MEDIUM
class Solution:
    def customSortString(self, order: str, s: str) -> str:
        cnt = collections.Counter(s)
        ans = ""
        for ch in order:
            while cnt.get(ch, 0) and cnt[ch] > 0:
                ans += ch
                cnt[ch] -= 1
        '''
        'ch' will have been assigned value and can be called,
        even if it in the last for loop and for loop ended
        print(ch)
        '''
        for ch in cnt:
            while cnt[ch] != 0:
                ans += ch
                cnt[ch] -= 1
        return ans

    def customSortString(self, order: str, s: str) -> str:
        cnt, ans = collections.Counter(s), ""
        for ch in order:
            if ch in cnt:
                ans += ch * cnt[ch]
                cnt.pop(ch)

        return ans + "".join(ch * cnt[ch] for ch in cnt)


# 794 - Valid Tic-Tac-Toe State - MEDIUM
class Solution:
    def validTicTacToe(self, board: List[str]) -> bool:

        return


# 797 - All Paths From Source to Target - MEDIUM
class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        def dfs(cur: int, path: List[int]):
            if cur == len(graph) - 1:
                ret.append(path)
            else:
                for i in graph[cur]:
                    dfs(i, path + [i])
            return

        ret = []
        dfs(0, [0])
        return ret

    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        stack, ret = [(0, [0])], []
        while stack:
            cur, path = stack.pop()
            if cur == len(graph) - 1:
                ret.append(path)
            for nei in graph[cur]:
                stack.append((nei, path + [nei]))
        return ret


# 798

# 799
