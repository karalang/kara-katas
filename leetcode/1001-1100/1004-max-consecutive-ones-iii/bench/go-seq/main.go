// Benchmark: LeetCode #1004 Max Consecutive Ones III -- the ★ arm, a
// sliding window, on arrays of 100000 numbers, LeetCode's longest.
// Mirrors longest_ones.kara, .c, .rs and .py.
package main

import "fmt"

func longestOnes(nums []int64, k int64) int64 {
	left, zeros, best := 0, int64(0), int64(0)
	for right := 0; right < len(nums); right++ {
		if nums[right] == 0 {
			zeros++
		}
		for zeros > k {
			if nums[left] == 0 {
				zeros--
			}
			left++
		}
		if int64(right-left+1) > best {
			best = int64(right - left + 1)
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const rounds, n = int64(30), int64(100000)
	seed := int64(1004)
	arrays := make([][]int64, 20)
	for t := int64(0); t < 20; t++ {
		nums := make([]int64, n)
		for j := range nums {
			if nextRandom(&seed)%8 < t%7+1 {
				nums[j] = 1
			}
		}
		arrays[t] = nums
	}
	total, check := int64(0), int64(0)
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < 20; i++ {
			t := (r + i) % 20
			k := (r*37 + t*101) % 3000
			got := longestOnes(arrays[t], k)
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 arrays of %d numbers: answers sum to %d, checksum %d\n", rounds, n, total, check)
}
