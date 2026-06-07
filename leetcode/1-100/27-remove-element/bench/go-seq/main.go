// LeetCode 27 — two-pointer in-place Remove Element, Go seq mirror.
package main

import "fmt"

func removeElement(nums []int64, length int64, val int64) int64 {
	k := int64(0)
	for i := int64(0); i < length; i++ {
		if nums[i] != val {
			nums[k] = nums[i]
			k++
		}
	}
	return k
}

func main() {
	const N = 2_000_000
	const val = int64(0)

	original := make([]int64, N)
	state := int64(1)
	for i := 0; i < N; i++ {
		state = (state*1103515245 + 12345) % 2147483648
		if (state/65536)%2 == 1 {
			original[i] = int64(i) + 1
		} else {
			original[i] = 0
		}
	}
	workspace := make([]int64, N)

	var sum int64
	for iter := 0; iter < 10; iter++ {
		for p := 0; p < N; p++ {
			workspace[p] = original[p]
		}
		k := removeElement(workspace, N, val)
		sum += k + workspace[k-1]
	}
	fmt.Println(sum)
}
