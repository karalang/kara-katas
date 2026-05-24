// LeetCode 88 — two-pointer-from-back Merge Sorted Array, Go seq mirror.
package main

import "fmt"

func merge(nums1 []int64, m int64, nums2 []int64, n int64) {
	i := m - 1
	j := n - 1
	k := m + n - 1
	for j >= 0 {
		if i >= 0 && nums1[i] > nums2[j] {
			nums1[k] = nums1[i]
			i--
		} else {
			nums1[k] = nums2[j]
			j--
		}
		k--
	}
}

func main() {
	const M = 1_000_000
	const N = 1_000_000
	const total = M + N

	prefixA := make([]int64, M)
	for i := 0; i < M; i++ {
		prefixA[i] = int64(2 * i)
	}
	b := make([]int64, N)
	for i := 0; i < N; i++ {
		b[i] = int64(2*i + 1)
	}
	workspace := make([]int64, total)

	var sum int64
	for iter := 0; iter < 10; iter++ {
		copy(workspace[:M], prefixA)
		merge(workspace, M, b, N)
		sum += workspace[total-1]
	}
	fmt.Println(sum)
}
