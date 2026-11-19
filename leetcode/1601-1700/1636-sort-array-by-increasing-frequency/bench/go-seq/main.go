// LeetCode #1636: Sort Array by Increasing Frequency -- the bench's Go
// mirror: the ★ arm on 50000 random arrays of 100 values from -100 to 100,
// all drawn first.
package main

import (
	"fmt"
	"sort"
)

func frequencySort(nums []int32) []int32 {
	count := map[int32]int64{}
	for _, x := range nums {
		count[x]++
	}
	sorted := append([]int32(nil), nums...)
	sort.SliceStable(sorted, func(i, j int) bool {
		a, b := sorted[i], sorted[j]
		if count[a] != count[b] {
			return count[a] < count[b]
		}
		return a > b
	})
	return sorted
}

var seed int64 = 1636

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int32, 50000)
	for i := range arrays {
		arrays[i] = make([]int32, 100)
		for k := range arrays[i] {
			arrays[i][k] = int32(nextRandom()%201 - 100)
		}
	}
	var check int64
	for _, nums := range arrays {
		for _, x := range frequencySort(nums) {
			check = (check*31 + int64(x) + 1000) % 1000000007
		}
	}
	fmt.Printf("50000 arrays of 100 values: checksum %d\n", check)
}
