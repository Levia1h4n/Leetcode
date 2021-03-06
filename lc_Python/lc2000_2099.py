import collections, bisect, itertools, functools, math, heapq, re
from typing import List


# 2000 - Reverse Prefix of Word - EASY
class Solution:
    def reversePrefix(self, word: str, ch: str) -> str:
        idx = -1
        for i in range(len(word)):
            if word[i] == ch:
                idx = i
                break
        return word[: idx + 1][::-1] + word[idx + 1 :]

    def reversePrefix(self, word: str, ch: str) -> str:
        i = word.find(ch) + 1
        return word[:i][::-1] + word[i:]


# 2006 - Count Number of Pairs With Absolute Difference K - EASY
class Solution:
    def countKDifference(self, nums: List[int], k: int) -> int:
        seen, counter = collections.defaultdict(int), 0
        for num in nums:
            counter += seen[num - k] + seen[num + k]
            seen[num] += 1
        return counter

    def countKDifference(self, nums: List[int], k: int) -> int:
        ans, dic = 0, {}
        for n in nums:
            if n - k in dic:
                ans += dic[n - k]
            if n + k in dic:
                ans += dic[n + k]
            dic[n] = dic.get(n, 0) + 1
        return ans


# 2013 - Detect Squares - MEDIUM
class DetectSquares:
    def __init__(self):
        self.samex = collections.defaultdict(collections.Counter)

    def add(self, point: List[int]) -> None:
        x, y = point
        self.samex[x][y] += 1
        return

    def count(self, point: List[int]) -> int:
        x, y = point
        ans = 0

        if x not in self.samex:
            return 0
        samex = self.samex[x]
        for k, diffy in self.samex.items():
            if k != x:
                d = k - x
                ans += diffy[y] * samex[y + d] * diffy[y + d]
                ans += diffy[y] * samex[y - d] * diffy[y - d]
        return ans


# 2016 - Maximum Difference Between Increasing Elements - EASY
class Solution:
    def maximumDifference(self, nums: List[int]) -> int:
        ans, mi = 0, math.inf
        for n in nums:
            mi = min(mi, n)
            ans = max(ans, n - mi)
        return ans if ans > 0 else -1

    def maximumDifference(self, nums: List[int]) -> int:
        ans, premin = -1, nums[0]
        for i in range(1, len(nums)):
            if nums[i] > premin:
                ans = max(ans, nums[i] - premin)
            else:
                premin = nums[i]
        return ans


# 2022 - Convert 1D Array Into 2D Array - EASY
class Solution:
    def construct2DArray(self, original: List[int], m: int, n: int) -> List[List[int]]:
        if len(original) != m * n:
            return []
        ans = []
        for i in range(0, len(original), n):
            ans.append([x for x in original[i : i + n]])
        return ans

    def construct2DArray(self, original: List[int], m: int, n: int) -> List[List[int]]:
        return (
            [original[i : i + n] for i in range(0, len(original), n)]
            if len(original) == m * n
            else []
        )


# 2024 - Maximize the Confusion of an Exam - MEDIUM
class Solution:
    def maxConsecutiveAnswers(self, s: str, k: int) -> int:
        d = collections.defaultdict(int)
        l = 0
        for r in range(len(s)):
            d[s[r]] += 1
            if min(d["T"], d["F"]) > k:
                d[s[l]] -= 1
                l += 1
        return len(s) - l
        # see lc1438, similar reason
        # the length of window will not decrease
        return r - l + 1

    # the length of window will decrease
    def maxConsecutiveAnswers(self, s: str, k: int) -> int:
        d = collections.defaultdict(int)
        l = ans = 0
        for r in range(len(s)):
            d[s[r]] += 1
            while min(d["T"], d["F"]) > k:
                d[s[l]] -= 1
                l += 1
            ans = max(ans, r - l + 1)
        return ans


# 2028 - Find Missing Observations - MEDIUM
class Solution:
    def missingRolls(self, rolls: List[int], mean: int, n: int) -> List[int]:
        m = len(rolls)
        t = (m + n) * mean - sum(rolls)
        if t > n * 6 or t < n:
            return []
        a = [0] * n
        while t:
            if t > n:
                for i in range(n):
                    a[i] += 1
                t -= n
            else:
                for i in range(t):
                    a[i] += 1
                t -= t
        return a

    def missingRolls(self, rolls: List[int], mean: int, n: int) -> List[int]:
        x = mean * (n + len(rolls)) - sum(rolls)
        if not n <= x <= n * 6:
            return []
        d, mod = divmod(x, n)
        return [d + 1] * mod + [d] * (n - mod)


# 2029 - Stone Game IX - MEDIUM
class Solution:
    def stoneGameIX(self, stones: List[int]) -> bool:
        d = [0, 0, 0]
        for n in stones:
            d[n % 3] += 1
        if d[0] % 2 == 0:
            return d[1] != 0 and d[2] != 0
        return d[2] > d[1] + 2 or d[1] > d[2] + 2


# 2034 - Stock Price Fluctuation - MEDIUM
class StockPrice:
    def __init__(self):
        self.maxPrice = []
        self.minPrice = []
        self.timePrice = {}
        self.maxTimestamp = 0

    def update(self, timestamp: int, price: int) -> None:
        heapq.heappush(self.maxPrice, (-price, timestamp))
        heapq.heappush(self.minPrice, (price, timestamp))
        self.timePrice[timestamp] = price
        self.maxTimestamp = max(self.maxTimestamp, timestamp)

    def current(self) -> int:
        return self.timePrice[self.maxTimestamp]

    def maximum(self) -> int:
        while True:
            price, timestamp = self.maxPrice[0]
            if -price == self.timePrice[timestamp]:
                return -price
            heapq.heappop(self.maxPrice)

    def minimum(self) -> int:
        while True:
            price, timestamp = self.minPrice[0]
            if price == self.timePrice[timestamp]:
                return price
            heapq.heappop(self.minPrice)


# 2038 - Remove Colored Pieces if Both Neighbors are the Same Color - MEDIUM
class Solution:
    def winnerOfGame(self, c: str) -> bool:
        a = b = 0
        for i in range(1, len(c) - 1):
            if c[i - 1] == c[i] == c[i + 1] == "A":
                a += 1
            elif c[i - 1] == c[i] == c[i + 1] == "B":
                b += 1
        return a > b


# 2039 - The Time When the Network Becomes Idle - MEDIUM
class Solution:
    # O(m + n) / O(m + n), m = len(edges)
    def networkBecomesIdle(self, edges: List[List[int]], p: List[int]) -> int:
        n = len(p)
        g = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)
        vis = [False] * n
        vis[0] = True
        q = collections.deque([0])
        ans = 0
        d = 1
        while q:
            for _ in range(len(q)):
                u = q.popleft()
                for v in g[u]:
                    if vis[v]:
                        continue
                    vis[v] = True
                    q.append(v)
                    ans = max(ans, (d * 2 - 1) // p[v] * p[v] + d * 2 + 1)
            d += 1
        return ans

    def networkBecomesIdle(self, edges: List[List[int]], p: List[int]) -> int:
        g = {}
        for u, v in edges:
            g.setdefault(u, []).append(v)
            g.setdefault(v, []).append(u)
        dist = [-1] * len(g)
        dist[0] = 0
        val = 0
        q = [0]
        while q:
            val += 1
            new = []
            for u in q:
                for v in g[u]:
                    if dist[v] == -1:
                        dist[v] = val
                        new.append(v)
            q = new
        ans = 0
        for i in range(1, len(p)):
            d = 2 * dist[i]
            s = 0
            if d <= p[i]:
                s = d + 1
            else:
                s = d + d - (d - 1) % p[i]
            ans = max(ans, s)
        return ans


# 2043 - Simple Bank System - MEDIUM
class Bank:
    def __init__(self, balance: List[int]):
        self.b = balance
        self.n = len(balance)

    def transfer(self, a1: int, a2: int, money: int) -> bool:
        if a1 > self.n or a2 > self.n or self.b[a1 - 1] < money:
            return False
        self.b[a1 - 1] -= money
        self.b[a2 - 1] += money
        return True

    def deposit(self, a: int, money: int) -> bool:
        if a > self.n:
            return False
        self.b[a - 1] += money
        return True

    def withdraw(self, a: int, money: int) -> bool:
        if a > self.n or self.b[a - 1] < money:
            return False
        self.b[a - 1] -= money
        return True


# 2044 - Count Number of Maximum Bitwise-OR Subsets - MEDIUM
class Solution:
    # O(2^n * n) / O(1)
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        def backtrack(arr: List[int], path: List[int]):
            t = 0
            for n in path:
                t |= n
            if t > self.mx:
                self.mx = t
                self.ans = 1
            elif t == self.mx:
                self.ans += 1
            for i in range(len(arr)):
                backtrack(arr[i + 1 :], path + [arr[i]])
            return

        self.mx = 0
        self.ans = 0
        backtrack(nums, [])
        return self.ans

    # O(2^n * n) / O(1), bitmask
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        ans = 0
        mx = 0
        for n in nums:
            mx |= n
        for state in range(1, 1 << len(nums)):
            t = 0
            for i in range(len(nums)):
                if state & 1:
                    t |= nums[i]
                state >>= 1
            if t == mx:
                ans += 1
        return ans

    def countMaxOrSubsets(self, nums: List[int]) -> int:
        target = 0
        for num in nums:
            target |= num

        @functools.lru_cache(None)
        def dfs(i, cur):
            if cur == target:
                return 2 ** (len(nums) - i)
            elif i == len(nums):
                return 0
            return dfs(i + 1, cur) + dfs(i + 1, cur | nums[i])

        return dfs(0, 0)

    # Similar to knapsack problem, but use bitwise-or sum instead of math sum.
    # O(mn) / O(m), m = max(nums)
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        cnt = collections.Counter([0])
        target = 0
        for n in nums:
            target |= n
            for k, v in list(cnt.items()):
                cnt[k | n] += v
        return cnt[target]

    def countMaxOrSubsets(self, nums: List[int]) -> int:
        dp = collections.Counter([0])
        for n in nums:
            for k, v in list(dp.items()):
                dp[k | n] += v
        return dp[max(dp)]


# 2045 - Second Minimum Time to Reach Destination - HARD
class Solution:
    def secondMinimum(
        self, n: int, edges: List[List[int]], time: int, change: int
    ) -> int:
        g = [[] for _ in range(n + 1)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)
        dist = [-1 for _ in range(n + 1)]
        dist[1] = 0
        dq = collections.deque([1])
        while dq:
            u = dq.popleft()
            for v in g[u]:
                if dist[v] == -1:
                    dq.append(v)
                    dist[v] = dist[u] + 1
        exist = False
        dq.append(n)
        while not exist and dq:
            u = dq.popleft()
            for v in g[u]:
                if dist[v] == dist[u]:
                    exist = True
                    break
                elif dist[v] == dist[u] - 1:
                    dq.append(v)
        d = dist[n] + 1 if exist else dist[n] + 2
        ans = 0
        for i in range(d):
            ans += time
            if (ans // change) % 2 == 1 and i != d - 1:
                ans += change - ans % change
        return ans

    # TODO
    def secondMinimum(
        self, n: int, edges: List[List[int]], time: int, change: int
    ) -> int:
        dis, dis2 = [float("inf")] * (n + 1), [float("inf")] * (n + 1)
        graph = collections.defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        dis[1] = 0
        dq = collections.deque([(0, 1)])
        while dq:
            cost, node = dq.popleft()
            for nei in graph[node]:
                new_cost = cost + time
                if (cost // change) % 2 == 1:
                    new_cost += change - (cost % change)
                if dis[nei] > new_cost:
                    dis2[nei], dis[nei] = dis[nei], new_cost
                    dq.append((new_cost, nei))
                elif dis[nei] < new_cost < dis2[nei]:
                    dis2[nei] = new_cost
                    dq.append((new_cost, nei))
        return dis2[n]


# 2047 - Number of Valid Words in a Sentence - EASY
class Solution:
    def countValidWords(self, sentence: str) -> int:
        return sum(
            bool(re.match(r"[a-z]*([a-z]-[a-z]+)?[!.,]?$", w)) for w in sentence.split()
        )

    def countValidWords(self, sentence: str) -> int:
        def valid(s: str) -> bool:
            hasHyphens = False
            for i, ch in enumerate(s):
                if ch.isdigit() or ch in "!.," and i < len(s) - 1:
                    return False
                if ch == "-":
                    if (
                        hasHyphens
                        or i == 0
                        or i == len(s) - 1
                        or not s[i - 1].islower()
                        or not s[i + 1].islower()
                    ):
                        return False
                    hasHyphens = True
            return True

        return sum(valid(s) for s in sentence.split())


# 2049 - Count Nodes With the Highest Score - MEDIUM
class Solution:
    def countHighestScoreNodes(self, parents: List[int]) -> int:
        g = collections.defaultdict(list)
        for i, v in enumerate(parents):
            g[v].append(i)

        def post(r):
            nonlocal ans, mx
            # if len(g[r]) == 0:
            #     if n - 1 > mx:
            #         ans, mx = 1, n - 1
            #     elif n - 1 == mx:
            #         ans += 1
            #     return 1
            p = 1
            top = n - 1
            child = 0
            for node in g[r]:
                ch = post(node)
                child += ch
                top -= ch
                p *= max(ch, 1)
            p *= max(top, 1)
            if p > mx:
                ans = 1
                mx = p
            elif p == mx:
                ans += 1
            return child + 1

        ans = mx = 0
        n = len(parents)
        post(0)
        return ans

    def countHighestScoreNodes(self, parents: List[int]) -> int:
        n = len(parents)
        g = collections.defaultdict(list)
        for i, p in enumerate(parents):
            g[p].append(i)
        mx, ans = 0, 0

        def dfs(node):
            left = dfs(g[node][0]) if g[node] else 0
            right = dfs(g[node][1]) if len(g[node]) == 2 else 0
            nonlocal mx, ans
            if (
                score := max(1, (n - left - right - 1)) * max(1, left) * max(1, right)
            ) > mx:
                mx, ans = score, 1
            elif score == mx:
                ans += 1
            return left + right + 1

        dfs(0)
        return ans

    def countHighestScoreNodes(self, parents: List[int]) -> int:
        n = len(parents)
        children = [[] for _ in range(n)]
        for node, p in enumerate(parents):
            if p != -1:
                children[p].append(node)
        maxScore, cnt = 0, 0

        def dfs(node: int) -> int:
            score = 1
            size = n - 1
            for ch in children[node]:
                sz = dfs(ch)
                score *= sz
                size -= sz
            if node != 0:
                score *= size
            nonlocal maxScore, cnt
            if score == maxScore:
                cnt += 1
            elif score > maxScore:
                maxScore, cnt = score, 1
            return n - size

        dfs(0)
        return cnt


# 2055 - Plates Between Candles - MEDIUM
class Solution:
    def platesBetweenCandles(self, s: str, queries: List[List[int]]) -> List[int]:
        n = len(s)
        preSum = [0] * n
        summ = 0
        left = [0] * n
        l = -1
        for i, ch in enumerate(s):
            if ch == "*":
                summ += 1
            else:
                l = i
            preSum[i] = summ
            left[i] = l
        right = [0] * n
        r = -1
        for i in range(n - 1, -1, -1):
            if s[i] == "|":
                r = i
            right[i] = r
        ans = [0] * len(queries)
        for i, (x, y) in enumerate(queries):
            x, y = right[x], left[y]
            if x >= 0 and y >= 0 and x < y:
                ans[i] = preSum[y] - preSum[x]
        return ans

    # O(n + Qlogn) / O(n + Q)
    def platesBetweenCandles(self, s: str, queries: List[List[int]]) -> List[int]:
        arr = [i for i, c in enumerate(s) if c == "|"]
        ans = []
        for a, b in queries:
            i = bisect.bisect_left(arr, a)
            j = bisect.bisect_right(arr, b) - 1
            ans.append((arr[j] - arr[i]) - (j - i) if i < j else 0)
        return ans
