from typing import List
import collections


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


# 786 - K-th Smallest Prime Fraction - HARD
class Solution:
    def kthSmallestPrimeFraction(self, arr: List[int], k: int) -> List[int]:
        div = []
        for i in range(len(arr) - 1):
            for j in range(i + 1, len(arr)):
                div.append((arr[i], arr[j]))
        div.sort(key=lambda x: x[0] / x[1])
        return div[k - 1]


class Solution:
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


class Solution:
    def customSortString(self, order: str, s: str) -> str:
        cnt, ans = collections.Counter(s), ""
        for ch in order:
            if ch in cnt:
                ans += ch * cnt[ch]
                cnt.pop(ch)

        return ans + "".join(ch * cnt[ch] for ch in cnt)


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


class Solution:
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
