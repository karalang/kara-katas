// LeetCode #1313 bench, Go: the ★ arm (the list read two numbers at a time,
// each pair's value pushed as many times as its count) on the same 100
// lists and 2000 passes.
package main

import "fmt"

func decompressRLEList(nums []int64) []int64 {
	var out []int64
	for i := 0; i < len(nums); i += 2 {
		for k := int64(0); k < nums[i]; k++ {
			out = append(out, nums[i+1])
		}
	}
	return out
}

var seed int64 = 1313

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int64, 100)
	for l := range lists {
		nums := make([]int64, 100)
		for k := range nums {
			nums[k] = 1 + nextRandom()%100
		}
		lists[l] = nums
	}
	var check int64
	for pass := int64(0); pass < 2000; pass++ {
		for l := 0; l < 100; l++ {
			lists[l][2*(check%50)] = 1 + (check/7)%100
			lists[l][2*((check/11)%50)+1] = 1 + (check/13)%100
			got := decompressRLEList(lists[l])
			n := int64(len(got))
			check = (check*31 + n) % 1000000007
			check = (check*31 + got[check%n]) % 1000000007
			check = (check*31 + got[(check/3)%n] + pass) % 1000000007
		}
	}
	fmt.Printf("2000 passes over 100 lists of 50 pairs: checksum %d\n", check)
}
