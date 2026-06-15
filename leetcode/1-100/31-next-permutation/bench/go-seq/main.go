// LeetCode #31 bench — Go (mirror of next_permutation.kara).
//
// Canonical four-move next-permutation, enumerating all K! permutations REPEAT
// times and folding a rolling checksum (single goroutine — seq lane).
package main

import "fmt"

func nextPermutation(nums []int64, length int) {
	i := length - 2
	for i >= 0 && nums[i] >= nums[i+1] {
		i--
	}
	if i >= 0 {
		j := length - 1
		for nums[j] <= nums[i] {
			j--
		}
		nums[i], nums[j] = nums[j], nums[i]
	}
	lo, hi := i+1, length-1
	for lo < hi {
		nums[lo], nums[hi] = nums[hi], nums[lo]
		lo++
		hi--
	}
}

func main() {
	const k = 10
	const fact int64 = 3628800 // 10!
	const repeat int64 = 8
	const modulus int64 = 2147483647 // 2^31 - 1

	nums := []int64{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	var acc int64 = 0

	for r := int64(0); r < repeat; r++ {
		for step := int64(0); step < fact; step++ {
			var h int64 = 0
			for i := 0; i < k; i++ {
				h = (h*131 + nums[i]) % modulus
			}
			acc = (acc + h) % modulus
			nextPermutation(nums, k)
		}
	}

	fmt.Println(acc)
}
