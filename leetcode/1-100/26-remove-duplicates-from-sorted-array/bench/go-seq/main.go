// LeetCode 26 — two-pointer in-place Remove Duplicates, Go seq mirror.
package main

import "fmt"

func removeDuplicates(nums []int64, length int64) int64 {
	if length == 0 {
		return 0
	}
	k := int64(1)
	for i := int64(1); i < length; i++ {
		if nums[i] != nums[k-1] {
			nums[k] = nums[i]
			k++
		}
	}
	return k
}

func main() {
	const N = 2_000_000

	original := make([]int64, N)
	state := int64(1)
	for i := 1; i < N; i++ {
		state = (state*1103515245 + 12345) % 2147483648
		original[i] = original[i-1] + (state/65536)%2
	}
	workspace := make([]int64, N)

	var sum int64
	for iter := 0; iter < 10; iter++ {
		for p := 0; p < N; p++ {
			workspace[p] = original[p]
		}
		k := removeDuplicates(workspace, N)
		sum += k + workspace[k-1]
	}
	fmt.Println(sum)
}
