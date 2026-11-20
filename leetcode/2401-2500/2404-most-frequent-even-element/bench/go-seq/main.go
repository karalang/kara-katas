// LeetCode #2404: Most Frequent Even Element -- the bench, the ★ arm in
// Go: a map of counts of the even values, then every entry read for the
// most frequent and the smallest among equal counts.

package main

import "fmt"

var seed int64 = 2404

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mostFrequentEven(nums []int64) int64 {
	count := map[int64]int64{}
	for _, x := range nums {
		if x%2 == 0 {
			count[x]++
		}
	}
	best, most := int64(-1), int64(0)
	for x, c := range count {
		if c > most || c == most && x < best {
			best, most = x, c
		}
	}
	return best
}

func main() {
	arrays := make([][]int64, 200)
	for i := range arrays {
		nums := make([]int64, 2000)
		for j := range nums {
			nums[j] = nextRandom() % (1 + 50*int64(i))
		}
		arrays[i] = nums
	}
	var check int64
	for p := int64(0); p < 100; p++ {
		for _, nums := range arrays {
			check = (check*31 + mostFrequentEven(nums) + 1 + p) % 1000000007
		}
	}
	fmt.Printf("100 passes over 200 arrays of 2000 values: checksum %d\n", check)
}
