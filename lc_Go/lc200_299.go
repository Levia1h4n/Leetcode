package lc_Go

import "sort"

// 229 - Majority Element II - MEDIUM
// similar question: 169 Majority Element
// Boyer–Moore majority vote algorithm / using map to count works too
func majorityElement(nums []int) (ans []int) {
	if len(nums) == 1 {
		return nums
	}
	sort.Ints(nums)
	time, n := 1, len(nums)/3
	for i := 1; i < len(nums); i++ {
		if nums[i] != nums[i-1] {
			if time > n {
				ans = append(ans, nums[i-1])
			}
			time = 1
		} else {
			time++
		}
		if i == len(nums)-1 {
			if time > n {
				ans = append(ans, nums[i])
			}
		}
	}
	return
}
func majorityElement2(nums []int) (ans []int) {
	element1, element2 := 0, 0
	vote1, vote2 := 0, 0
	for _, num := range nums {
		if vote1 > 0 && num == element1 { // 如果该元素为第一个元素，则计数加1
			vote1++
		} else if vote2 > 0 && num == element2 { // 如果该元素为第二个元素，则计数加1
			vote2++
		} else if vote1 == 0 { // 选择第一个元素
			element1 = num
			vote1++
		} else if vote2 == 0 { // 选择第二个元素
			element2 = num
			vote2++
		} else { // 如果三个元素均不相同，则相互抵消1次
			vote1--
			vote2--
		}
	}
	cnt1, cnt2 := 0, 0
	for _, num := range nums {
		if vote1 > 0 && num == element1 {
			cnt1++
		}
		if vote2 > 0 && num == element2 {
			cnt2++
		}
	}
	// 检测元素出现的次数是否满足要求
	if vote1 > 0 && cnt1 > len(nums)/3 {
		ans = append(ans, element1)
	}
	if vote2 > 0 && cnt2 > len(nums)/3 {
		ans = append(ans, element2)
	}
	return
}

// 230 - Kth Smallest Element in a BST - MEDIUM
// inorder / use a slice to save all values / O(n) + O(n)
func kthSmallest(root *TreeNode, k int) int {
	var res []int
	var dfs func(r *TreeNode)
	dfs = func(root *TreeNode) {
		if root != nil {
			dfs(root.Left)
			res = append(res, root.Val)
			dfs(root.Right)
		}
	}
	dfs(root)
	return res[k-1]
}

// 237 - Delete Node in a Linked List - EASY
func deleteNode(node *ListNode) {
	node.Val = node.Next.Val
	node.Next = node.Next.Next
}

// 240 - Search a 2D Matrix II - MEDIUM
// search each row, then search each element from qualified row
func searchMatrix(matrix [][]int, target int) bool {
	for i := len(matrix) - 1; i >= 0; i-- {
		if matrix[i][0] <= target && target <= matrix[i][len(matrix[0])-1] {
			for j := 0; j < len(matrix[0]); j++ {
				if target == matrix[i][j] {
					return true
				}
			}
		}
	}
	return false
}

// Binary search
func searchMatrix2(matrix [][]int, target int) bool {
	for _, row := range matrix {
		i := sort.SearchInts(row, target)
		if i < len(row) && row[i] == target {
			return true
		}
	}
	return false
}

// Zigzag search
// from (0, n-1) to (n-1, 0) / remove one column or one row at each search
func searchMatrix3(matrix [][]int, target int) bool {
	m, n := len(matrix), len(matrix[0])
	x, y := 0, n-1
	for x < m && y >= 0 {
		if matrix[x][y] == target {
			return true
		}
		if matrix[x][y] > target {
			y--
		} else {
			x++
		}
	}
	return false
}
