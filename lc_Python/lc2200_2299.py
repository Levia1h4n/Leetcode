import bisect, collections, functools, math, itertools, heapq
from typing import List, Optional


# 2200 - Find All K-Distant Indices in an Array - EASY
class Solution:
    def findKDistantIndices(self, nums: List[int], key: int,
                            k: int) -> List[int]:
        ans = []
        n = len(nums)
        for i in range(n):
            for j in range(i - k, i + k + 1):
                if 0 <= j < n and nums[j] == key:
                    ans.append(i)
                    break
        return ans


# 2201 - Count Artifacts That Can Be Extracted - MEDIUM
class Solution:
    def digArtifacts(self, n: int, artifacts: List[List[int]],
                     dig: List[List[int]]) -> int:
        s = set((i, j) for i, j in dig)
        ans = 0
        for r1, c1, r2, c2 in artifacts:
            have = True
            f = False
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    if (r, c) not in s:
                        have = False
                        f = True
                        break
                if f:
                    break
            if have:
                ans += 1
        return ans


# 2202 - Maximize the Topmost Element After K Moves - MEDIUM
class Solution:
    def maximumTop(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 1 or k == 0:
            if k & 1:
                return -1
            else:
                return nums[0]

        f = max(nums[:k - 1]) if k > 1 else 0
        s = nums[k] if k < n else 0
        return max(f, s)


# 2203 - Minimum Weighted Subgraph With the Required Paths - HARD
class Solution:
    def minimumWeight(self, n: int, edges: List[List[int]], src1: int,
                      src2: int, dest: int) -> int:
        def dijkstra(g: List[List[tuple]], start: int) -> List[int]:
            dis = [math.inf] * n
            dis[start] = 0
            pq = [(0, start)]
            while pq:
                d, x = heapq.heappop(pq)
                if dis[x] < d:
                    continue
                for y, wt in g[x]:
                    new_d = dis[x] + wt
                    if new_d < dis[y]:
                        dis[y] = new_d
                        heapq.heappush(pq, (new_d, y))
            return dis

        g = [[] for _ in range(n)]
        rg = [[] for _ in range(n)]
        for x, y, wt in edges:
            g[x].append((y, wt))
            rg[y].append((x, wt))

        d1 = dijkstra(g, src1)
        d2 = dijkstra(g, src2)
        d3 = dijkstra(rg, dest)

        ans = min(sum(d) for d in zip(d1, d2, d3))
        return ans if ans < math.inf else -1

    def minimumWeight(self, n: int, edges: List[List[int]], src1: int,
                      src2: int, dest: int) -> int:
        g = collections.defaultdict(list)
        reverse_g = collections.defaultdict(list)
        for i, j, w in edges:
            g[i].append((j, w))
            reverse_g[j].append((i, w))

        def dijkstra(src: int, G: collections.defaultdict):
            dis = [math.inf] * n
            pq = [(0, src)]
            while pq:
                w, node = heapq.heappop(pq)
                if dis[node] <= w:  # see the different symbols between here and solution above
                    continue
                dis[node] = w
                for nxt, wt in G[node]:
                    if w + wt < dis[nxt]:  # and here
                        heapq.heappush(pq, (w + wt, nxt))
            return dis

        l1 = dijkstra(src1, g)
        l2 = dijkstra(src2, g)
        l3 = dijkstra(dest, reverse_g)
        ans = math.inf
        for i in range(n):
            ans = min(ans, l1[i] + l2[i] + l3[i])
        return ans if ans != math.inf else -1

    def minimumWeight(self, n: int, edges: List[List[int]], src1: int,
                      src2: int, dest: int) -> int:
        G1 = collections.defaultdict(list)
        G2 = collections.defaultdict(list)
        for a, b, w in edges:
            G1[a].append((b, w))
            G2[b].append((a, w))

        def dijkstra(graph: collections.defaultdict, src: int):
            pq = [(0, src)]
            t = {}
            while pq:
                time, node = heapq.heappop(pq)
                if node not in t:
                    t[node] = time
                    for v, w in graph[node]:
                        heapq.heappush(pq, (time + w, v))
            return [t.get(i, float("inf")) for i in range(n)]

        arr1 = dijkstra(G1, src1)
        arr2 = dijkstra(G1, src2)
        arr3 = dijkstra(G2, dest)

        ans = float("inf")
        for i in range(n):
            ans = min(ans, arr1[i] + arr2[i] + arr3[i])
        return ans if ans != float("inf") else -1


# 2206 - Divide Array Into Equal Pairs - EASY
class Solution:
    def divideArray(self, nums: List[int]) -> bool:
        # cnt = collections.Counter(nums)
        # for n in cnt:
        #     if cnt[n] & 1:
        #         return False
        # return True
        return all(v % 2 == 0 for _, v in collections.Counter(nums).items())
        return not any(v & 1 for _, v in collections.Counter(nums).items())


# 2207 - Maximize Number of Subsequences in a String - MEDIUM
class Solution:
    def maximumSubsequenceCount(self, t: str, p: str) -> int:
        a = ans = 0
        b = t.count(p[1])
        if p[1] == p[0]:
            ans = b * (b + 1) // 2
        else:
            for ch in t:
                if ch == p[0]:
                    ans += b
                    a += 1
                elif ch == p[1]:
                    # ans += a
                    b -= 1
            # ans //= 2
            ans += max(a, t.count(p[1]))
        return ans

    # O(n) / O(1)
    def maximumSubsequenceCount(self, t: str, p: str) -> int:
        ans = c1 = c2 = 0
        for ch in t:
            if ch == p[1]:
                ans += c1
                c2 += 1
            if ch == p[0]:  # two 'if' to handle the case where p[0] == p[1]
                c1 += 1
        return ans + max(c1, c2)


# 2208 - Minimum Operations to Halve Array Sum -  MEDIUM
class Solution:
    # O(n * logn + m * logn) / O(n), where m is the number of operations
    def halveArray(self, nums: List[int]) -> int:
        t = sum(nums)
        half = t / 2
        hp = [-n for n in nums]
        heapq.heapify(hp)  # nlogn
        ans = 0
        while t > half:
            n = -heapq.heappop(hp) / 2
            t -= n
            heapq.heappush(hp, -n)
            ans += 1
        return ans


# 2209 - Minimum White Tiles After Covering With Carpets - HARD
class Solution:
    # dp[i][j], means that consider the previous floor with length 'j',
    # 'i' carpets are used, the minimum remaining white tiles.
    # i == 0, not use carpet, dp[0][j] is the number of white tiles before index j
    # i != 0, dp[i][j] = min(dp[i][j-1] + isWhite[j], dp[i-1][j-carpetLen])
    # dp[i][j-1] + isWhite[j]: not use carpet in 'floor[j]'
    # dp[i-1][j-carpetLen]: use carpet in 'floor[j]'
    # O(nm) / O(nm), n = len(floor), m = numCarpets
    def minimumWhiteTiles(self, floor: str, ncp: int, l: int) -> int:
        n = len(floor)
        dp = [[0] * n for _ in range(ncp + 1)]
        dp[0][0] = 1 if floor[0] == '1' else 0
        isWhite = [0] * n
        for i in range(1, n):
            dp[0][i] = dp[0][i - 1]
            if floor[i] == '1':
                dp[0][i] += 1
                isWhite[i] = 1
        for i in range(1, ncp + 1):
            for j in range(n):
                # less than 'carpetLen' bricks will end up with 0 white bricks left after using the carpet
                if j < l:
                    dp[i][j] = 0
                else:
                    dp[i][j] = min(dp[i][j - 1] + isWhite[j], dp[i - 1][j - l])
        return dp[ncp][n - 1]

    def minimumWhiteTiles(self, floor: str, numCarpets: int,
                          carpetLen: int) -> int:
        # define dp[i][numCarpet]
        # choose use or not use
        # if use: dp[i][use] = dp[i+carpetLen][use-1]
        @functools.lru_cache(None)
        def dfs(i, num):
            if i >= len(floor): return 0
            res = float('inf')
            # use
            if num:
                res = dfs(i + carpetLen, num - 1)
            # not use
            res = min(res, (floor[i] == '1') + dfs(i + 1, num))
            return res

        return dfs(0, numCarpets)

    def minimumWhiteTiles(self, floor: str, numCarpets: int,
                          carpetLen: int) -> int:
        pre = [0]
        n = len(floor)
        for i in range(n):
            if floor[i] == '1':
                pre.append(pre[-1] + 1)
            else:
                pre.append(pre[-1])

        @functools.lru_cache(None)
        def dp(i, j):
            if i < 0:
                return 0
            if j == 0:
                return pre[i + 1]
            return min(
                dp(i - 1, j) + (1 if floor[i] == '1' else 0),
                dp(i - carpetLen, j - 1))

        return dp(n - 1, numCarpets)


# 2210 - Count Hills and Valleys in an Array - EASY
class Solution:
    def countHillValley(self, nums: List[int]) -> int:
        nums.append(math.inf)
        a = []
        for i in range(len(nums) - 1):
            if nums[i] != nums[i + 1]:
                a.append(nums[i])
        ans = 0
        for i in range(1, len(a) - 1):
            if a[i - 1] > a[i] < a[i + 1] or a[i - 1] < a[i] > a[i + 1]:
                ans += 1
        return ans


# 2211 - Count Collisions on a Road - MEDIUM
class Solution:
    def countCollisions(self, directions: str) -> int:
        s = []
        co = 0
        for ch in directions:
            if ch == 'L':
                if not s:
                    continue
                elif s[-1] == 'S':
                    co += 1
                elif s[-1] == 'R':
                    while s and s[-1] == 'R':
                        s.pop()
                        co += 1
                    co += 1
                    s.append('S')
            elif ch == 'R':
                s.append(ch)
            else:
                while s and s[-1] == 'R':
                    s.pop()
                    co += 1
                s.append('S')
        return co

    # All the cars that move to the middle will eventually collide
    def countCollisions(self, directions: str) -> int:
        return sum(d != 'S' for d in directions.lstrip('L').rstrip('R'))


# 2212 - Maximum Points in an Archery Competition - MEDIUM
# TODO
class Solution:
    # bitmasking. Enumerate the regions on which Bob wins,
    # which has a total of 2^12 different cases
    # O(2 ^ 12 * 12) / O(C)
    def maximumBobPoints(self, num: int, ali: List[int]) -> List[int]:
        ans = []
        mx = 0
        for i in range(1 << len(ali)):
            score, arrow, bob = 0, 0, [0] * 12
            for j in range(len(ali)):
                # if i & (1 << j):
                if i >> j & 1 == 1:
                    score += j
                    arrow += ali[j] + 1
                    bob[j] = ali[j] + 1
            if arrow > num:
                continue
            if score > mx:
                mx = score
                bob[0] += num - arrow  # has remaining arrow
                ans = bob
        return ans

    # O(2 * 12 * numArrows) / O(12 * numArrows)
    # There are total 12 * numArrows states, each state need at most 2 case (Lose or Win) to compute
    def maximumBobPoints(self, numArrows: int, ali: List[int]) -> List[int]:
        @functools.lru_cache(None)
        def dp(k, numArrows):
            if k == 12 or numArrows <= 0:
                return 0
            mx = dp(k + 1, numArrows)  # Bob Lose
            if numArrows > ali[k]:
                mx = max(mx, dp(k + 1, numArrows - ali[k] - 1) + k)  # Bob Win
            return mx

        # backtracking
        ans = [0] * 12
        remain = numArrows
        for k in range(12):
            # It means that section k was chosen where bob wins.
            # If dp(k, numArrows) == dp(k+1, numArrows),
            # then that would mean that maxScore didn't change
            # and hence bob didn't win at section k.
            # Else, it would mean that the maxScore changed,
            # implying that bob won at section k
            if dp(k, numArrows) != dp(k + 1, numArrows):  # If Bob win
                ans[k] = ali[k] + 1
                numArrows -= ans[k]
                remain -= ans[k]

        ans[0] += remain  # In case of having remain arrows then it means in all sections Bob always win
        # then we can distribute the remain to any section, here we simple choose first section.
        return ans

    def maximumBobPoints(self, numArrows: int, ali: List[int]) -> List[int]:
        ans = 0
        plan = [0] * 10

        def search(i, arrows, score, cur_plan):
            nonlocal ans, plan
            if i == len(ali):
                if score > ans:
                    ans = score
                    plan = cur_plan[:]
                return
            if ali[i] + 1 <= arrows:
                cur_plan.append(ali[i] + 1)
                search(i + 1, arrows - ali[i] - 1, score + i, cur_plan)
                cur_plan.pop()
            cur_plan.append(0)
            search(i + 1, arrows, score, cur_plan)
            cur_plan.pop()

        search(1, numArrows, 0, [])
        return [numArrows - sum(plan)] + plan

    # TLE, knapsack problem with path reduction
    def maximumBobPoints(self, numArrows: int, ali: List[int]) -> List[int]:
        f = [[0] * (numArrows + 1) for _ in range(12)]
        ans = [0] * 12
        for i in range(1, 12):
            a = ali[i]
            for j in range(1, numArrows + 1):
                if j < a + 1:
                    f[i][j] = f[i - 1][j]
                else:
                    f[i][j] = max(f[i - 1][j - a - 1] + i, f[i - 1][j])
        for i in range(11, 0, -1):
            if f[i][numArrows] > f[i - 1][numArrows]:
                ans[i] = ali[i] + 1
                numArrows -= ali[i] + 1
        ans[0] = numArrows
        return ans


# 2215 - Find the Difference of Two Arrays - EASY
class Solution:
    def findDifference(self, nums1, nums2):
        s1 = set(nums1)
        s2 = set(nums2)
        a = set()
        b = set()
        for n in nums1:
            if n not in s2:
                a.add(n)
        for n in nums2:
            if n not in s1:
                b.add(n)
        return [list(a), list(b)]

    def findDifference(self, nums1, nums2):
        s1, s2 = set(nums1), set(nums2)
        return [list(s1 - s2), list(s2 - s1)]

    def findDifference(self, nums1, nums2):
        return [list((s1 := set(nums1)) - (s2 := set(nums2))), list(s2 - s1)]


# 2216 - Minimum Deletions to Make Array Beautiful - MEDIUM
class Solution:
    # O(n) / O(n)
    # using the stack to simulate the process.
    # if the stack size is even, can add any value
    # if the stack size is odd, can not add the value the same as the top of stack
    # no need for a stack, use a variable to represent the parity of the stack
    def minDeletion(self, nums: List[int]) -> int:
        a = []
        for n in nums:
            if len(a) % 2 == 0 or n != a[-1]:
                a.append(n)
        return len(nums) - (len(a) - len(a) % 2)

    def minDeletion(self, a: List[int]) -> int:
        b = []
        for n in a:
            if len(b) % 2 == 1 and b[-1] == n:
                b.pop()
            b.append(n)
        if len(b) % 2 == 1:
            b.pop()
        return len(a) - len(b)

    def minDeletion(self, nums: List[int]) -> int:
        ans = []
        for n in nums:
            if len(ans) % 2 == 0 or ans[-1] != n:
                ans.append(n)
        if len(ans) % 2 == 1:
            ans.pop()
        return len(nums) - len(ans)

    # O(n) / O(1), greedy
    def minDeletion(self, nums: List[int]) -> int:
        flag = 0
        ans = 0
        for i in range(len(nums) - 1):
            if i % 2 == flag and nums[i] == nums[i + 1]:
                ans += 1
                flag = 1 - flag
        if (len(nums) - ans) % 2 == 1:
            ans += 1
        return ans

    # if the number can be the second of the pair, keep it
    # skip each pair
    def minDeletion(self, nums: List[int]) -> int:
        ans = i = 0
        while i < len(nums) - 1:
            if nums[i] == nums[i + 1]:
                ans += 1
            else:
                i += 1
            i += 1
        if (len(nums) - ans) % 2:
            ans += 1
        return ans

    # using a variable 'pre' to record the last element with even index.
    def minDeletion(self, nums: List[int]) -> int:
        ans = 0
        pre = -1
        for n in nums:
            if n == pre:
                ans += 1
            else:
                pre = n if pre < 0 else -1
        return ans + (pre >= 0)

    def minDeletion(self, nums: List[int]) -> int:
        ans = 0
        l = None
        for n in nums:
            if l is None:
                l = n
            elif l != n:
                l = None
                ans += 2
        return len(nums) - ans


# 2217 - Find Palindrome With Fixed Length - MEDIUM
class Solution:
    # O(n * L) / O(n * L)
    def kthPalindrome(self, queries: List[int], intLength: int) -> List[int]:
        base = 10**((intLength - 1) // 2)
        ans = [-1] * len(queries)
        for i, q in enumerate(queries):
            if q <= 9 * base:
                s = str(base + q - 1)
                s += s[-2::-1] if intLength % 2 else s[::-1]
                ans[i] = int(s)
        return ans

    def kthPalindrome(self, queries: List[int], l: int) -> List[int]:
        base = 10**((l - 1) // 2)
        ans = [q - 1 + base for q in queries]
        for i, a in enumerate(ans):
            a = str(a) + str(a)[-1 - l % 2::-1]
            ans[i] = int(a) if len(a) == l else -1
        return ans


# 2220 - Minimum Bit Flips to Convert Number - EASY
class Solution:
    def minBitFlips(self, start: int, goal: int) -> int:
        s = bin(start)[2:]  # bin() -> O(logn)
        g = bin(goal)[2:]
        if len(s) > len(g):
            g = '0' * (len(s) - len(g)) + g
        if len(s) < len(g):
            s = '0' * (len(g) - len(s)) + s
        ans = 0
        for i in range(len(s)):
            if s[i] != g[i]:
                ans += 1
        return ans

    # O(logM) / O(1), M = max(start, goal)
    def minBitFlips(self, start: int, goal: int) -> int:
        ans = 0
        xor = start ^ goal
        while xor:
            ans += xor & 1
            xor >>= 1
        return ans

    def minBitFlips(self, start: int, goal: int) -> int:
        ans = 0
        xor = start ^ goal
        while xor:
            ans += 1
            xor &= xor - 1
        return ans

    # python3.10: int.bit_count()
    def minBitFlips(self, start: int, goal: int) -> int:
        return (start ^ goal).bit_count()


# 2221. Find Triangular Sum of an Array - MEDIUM
class Solution:
    # O(n ^ 2) / O(1), in place
    def triangularSum(self, nums: List[int]) -> int:
        n = len(nums)
        while n > 1:
            for i in range(n - 1):
                nums[i] = (nums[i] + nums[i + 1]) % 10
            n -= 1
        return nums[0]


# 2222. Number of Ways to Select Buildings - MEDIUM
class Solution:
    def numberOfWays(self, s: str) -> int:
        ans = n0 = n1 = n01 = n10 = 0
        for ch in s:
            if ch == '1':
                n10 += n0
                ans += n01
                n1 += 1
            else:
                n01 += n1
                ans += n10
                n0 += 1
        return ans

    def numberOfWays(self, s: str) -> int:
        ans = n0 = 0
        t0 = s.count('0')
        for i, ch in enumerate(s):
            if ch == '1':
                ans += n0 * (t0 - n0)  # (left '0') * (right '0')
            else:
                n1 = i - n0
                ans += n1 * (len(s) - t0 - n1)  # (left '1') * (right '1')
                n0 += 1
        return ans

    # eg: 101, c: '101', b = '10', a = '1'
    def numberOfWays(self, s: str) -> int:
        def f(t: str) -> int:
            a = b = c = 0
            for ch in s:
                if ch == t[2]: c += b
                if ch == t[1]: b += a
                if ch == t[0]: a += 1
            return c

        return f('101') + f('010')


# 2231 - Largest Number After Digit Swaps by Parity - EASY
class Solution:
    # do not need to care about specific indices
    def largestInteger(self, num: int):
        arr = [int(i) for i in str(num)]
        odd = []
        even = []
        for i in arr:
            if i % 2 == 0:
                even.append(i)
            else:
                odd.append(i)
        odd.sort()
        even.sort()
        ans = 0
        for i in range(len(str(num))):
            if arr[i] % 2 == 0:
                ans = ans * 10 + even.pop()
            else:
                ans = ans * 10 + odd.pop()
        return ans

    def largestInteger(self, num: int) -> int:
        s = str(num)
        o, e = [], []
        for ch in s:
            if int(ch) % 2:
                o.append(ch)
            else:
                e.append(ch)
        o.sort()
        e.sort()
        ss = ''
        for ch in s:
            if int(ch) % 2:
                ss += o.pop()
            else:
                ss += e.pop()
        return int(ss)


# 2232 - Minimize Result by Adding Parentheses to Expression - MEDIUM
class Solution:
    def minimizeResult(self, expression: str) -> str:
        n1, n2 = expression.split('+')
        m = 1e99
        ans = None
        for i in range(len(n1)):
            a = 1 if i == 0 else int(n1[:i])
            s1 = str(a) if i != 0 else ''
            b = int(n1[i:])
            for j in range(len(n2)):
                c = int(n2[:j + 1])
                d = 1 if j == len(n2) - 1 else int(n2[j + 1:])
                s2 = str(d) if j != len(n2) - 1 else ''
                p = a * (b + c) * d
                if p < m:
                    m = p
                    ans = '%s(%d+%d)%s' % (s1, b, c, s2)
        return ans

    def minimizeResult(self, expression: str) -> str:
        a, b = expression.split('+')
        m = math.inf
        ans = None
        for i in range(len(a)):
            for j in range(1, len(b) + 1):
                s = '' if i == 0 else a[:i] + '*'
                s += '('
                s += a[i:]
                s += '+'
                s += b[:j]
                s += ')'
                if j != len(b):
                    s += '*' + b[j:]
                cur = eval(s)
                if cur < m:
                    m = cur
                    ans = s
        return ans.replace('*', '')


# 2233 - Maximum Product After K Increments - MEDIUM
class Solution:
    def maximumProduct(self, nums: List[int], k: int) -> int:
        cnt = collections.Counter(nums)
        pq = [(n, v) for n, v in cnt.items()]
        heapq.heapify(pq)
        while k:
            if k >= pq[0][1]:
                n, v = heapq.heappop(pq)
                k -= v
                n += 1
                if pq and pq[0][0] == n:
                    _, vv = heapq.heappop(pq)
                    heapq.heappush(pq, (n, v + vv))
                else:
                    heapq.heappush(pq, (n, v))
            else:
                n, v = heapq.heappop(pq)
                if pq and pq[0][0] == n + 1:
                    nn, vv = heapq.heappop(pq)
                    pq.append((nn, vv + k))
                    pq.append((n, v - k))
                else:
                    pq.append((n + 1, k))
                    pq.append((n, v - k))
                break
        ans = 1
        for i in range(len(pq)):
            ans *= pq[i][0]**pq[i][1]
        return ans % (10**9 + 7)

    def maximumProduct(self, nums: List[int], k: int) -> int:
        cnt = collections.Counter(nums)
        keys = sorted(list(cnt.keys()))
        i = keys[0]
        while k > 0:
            if k > cnt[i]:
                k -= cnt[i]
                cnt[i + 1] += cnt[i]
                cnt[i] = 0
                i += 1
            else:
                cnt[i + 1] += k
                cnt[i] -= k
                k = 0
        mod = 10**9 + 7
        ans = 1
        for i in cnt.keys():
            if cnt[i] > 0:
                ans *= i**cnt[i]
                ans %= mod
        return ans

    def maximumProduct(self, nums: List[int], k: int) -> int:
        mod = 10**9 + 7
        heapq.heapify(nums)
        while k:
            heapq.heapreplace(nums, nums[0] + 1)
            k -= 1
        ans = 1
        for n in nums:
            ans = ans * n % mod
        return ans

    def maximumProduct(self, nums: List[int], k: int) -> int:
        heapq.heapify(nums)
        for _ in range(k):
            heapq.heapreplace(nums, nums[0] + 1)
        return functools.reduce(lambda x, y: x * y % 1000000007, nums)


# 2234 - Maximum Total Beauty of the Gardens - HARD
class Solution:
    # O(n * logn) / O(1)
    def maximumBeauty(self, f: List[int], newFlowers: int, target: int,
                      full: int, partial: int) -> int:
        f.sort()
        n = len(f)
        if f[0] >= target:
            return n * full
        leftFlowers = newFlowers
        for i in range(n):
            leftFlowers -= max(target - f[i], 0)
            f[i] = min(f[i], target)
        ans = x = sumFlowers = 0
        for i in range(n + 1):
            if leftFlowers >= 0:
                while x < i and f[x] * x - sumFlowers <= leftFlowers:
                    sumFlowers += f[x]
                    x += 1
                beauty = (n - i) * full
                if x:  # for division
                    beauty += min(
                        (leftFlowers + sumFlowers) // x, target - 1) * partial
                ans = max(ans, beauty)
            if i < n:
                leftFlowers += target - f[i]
        return ans

    def maximumBeauty(self, f: List[int], newFlowers: int, target: int,
                      full: int, partial: int) -> int:
        f = [min(target, x) for x in f]
        f.sort()
        n = len(f)
        if f[0] == target:
            return full * n
        if newFlowers >= target * n - sum(f):
            return max(full * n, full * (n - 1) + partial * (target - 1))
        cost = [0]
        for i in range(1, n):
            pre = cost[-1]
            cost.append(pre + i * (f[i] - f[i - 1]))
        j = n - 1
        while f[j] == target:
            j -= 1
        ans = 0
        while newFlowers >= 0:
            idx = min(j, bisect.bisect_right(cost, newFlowers) - 1)
            bar = f[idx] + (newFlowers - cost[idx]) // (idx + 1)
            ans = max(ans, bar * partial + (n - j - 1) * full)
            newFlowers -= target - f[j]
            j -= 1
        return ans


# 2239 - Find Closest Number to Zero - EASY
class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        return sorted(nums, key=lambda x: (abs(x), -x))[0]

        return max([-abs(n), n] for n in nums)[1]
        return -min([abs(n), -n] for n in nums)[1]


# 2240 - Number of Ways to Buy Pens and Pencils - MEDIUM
class Solution:
    def waysToBuyPensPencils(self, t: int, c1: int, c2: int) -> int:
        ans = 0
        for i in range(0, t + 1, c1):
            ans += (t - i) // c2 + 1
        return ans

        return sum(((t - i * c1) // c2 + 1) for i in range(t // c1 + 1))
        return sum(((t - i) // c2 + 1) for i in range(0, t + 1, c1))

    def waysToBuyPensPencils(self, t: int, c1: int, c2: int) -> int:
        ans = 0
        while t >= 0:
            ans += t // c2 + 1
            t -= c1
        return ans


# 2241 - Design an ATM Machine - MEDIUM
class ATM:
    def __init__(self):
        self.b = [0, 0, 0, 0, 0]
        self.m = [20, 50, 100, 200, 500]

    def deposit(self, banknotesCount: List[int]) -> None:
        for i in range(5):
            self.b[i] += banknotesCount[i]
        return

    def withdraw(self, amount: int) -> List[int]:
        ans = [0, 0, 0, 0, 0]
        for i in range(4, -1, -1):
            if amount >= self.m[i] * self.b[i]:
                amount -= self.m[i] * self.b[i]
                ans[i] = self.b[i]
            else:
                ans[i] = amount // self.m[i]
                amount %= self.m[i]

        # for i in range(4, -1, -1):
        #     v = min(self.b[i], amount // self.m[i])
        #     ans[i] = v
        #     amount -= v * self.m[i]

        if amount == 0:
            for i in range(5):
                self.b[i] -= ans[i]
        return ans if amount == 0 else [-1]
