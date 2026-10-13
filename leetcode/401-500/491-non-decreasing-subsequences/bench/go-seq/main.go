// Benchmark for #491: Go mirror of the ★ arm (backtracking); see
// ../non_decreasing_subsequences.kara.
package main

import "fmt"

func extend(nums []int64, from int, current *[]int64, out *[][]int64) {
	if len(*current) >= 2 {
		*out = append(*out, append([]int64(nil), *current...))
	}
	tried := map[int64]bool{}
	for i := from; i < len(nums); i++ {
		if tried[nums[i]] {
			continue
		}
		if len(*current) == 0 || nums[i] >= (*current)[len(*current)-1] {
			tried[nums[i]] = true
			*current = append(*current, nums[i])
			extend(nums, i+1, current, out)
			*current = (*current)[:len(*current)-1]
		}
	}
}

func findSubsequences(nums []int64) [][]int64 {
	var out [][]int64
	var current []int64
	extend(nums, 0, &current, &out)
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 3000 arrays of 15 numbers, the k-th from k / 2 to k / 2 + 3, so
	// they mostly rise, built once, then each solved once.
	var arrays [][]int64
	var seed int64 = 491
	for a := 0; a < 3000; a++ {
		nums := make([]int64, 0, 15)
		for k := int64(0); k < 15; k++ {
			nums = append(nums, k/2+nextRandom(&seed)%4)
		}
		arrays = append(arrays, nums)
	}
	total := 0
	var checksum int64
	for _, nums := range arrays {
		out := findSubsequences(nums)
		total += len(out)
		for _, s := range out {
			for _, x := range s {
				checksum = (checksum*31 + x + 7) % 1000000007
			}
			checksum = (checksum*31 + 15) % 1000000007
		}
	}
	fmt.Printf("3000 arrays of 15: %d subsequences, checksum %d\n", total, checksum)
}
