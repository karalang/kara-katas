// LeetCode #1512: Number of Good Pairs -- the bench: 50 arrays of 200000
// numbers from 1 to 100 built once, then each counted four times by the
// ★ arm.
package main

import "fmt"

func numIdenticalPairs(nums []int64) int64 {
	var seen [101]int64
	var pairs int64
	for _, x := range nums {
		pairs += seen[x]
		seen[x]++
	}
	return pairs
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1512)
	arrays := make([][]int64, 50)
	for a := range arrays {
		arrays[a] = make([]int64, 200000)
		for i := range arrays[a] {
			arrays[a][i] = nextRandom(&seed)%100 + 1
		}
	}
	var check int64
	for r := 0; r < 4; r++ {
		for _, nums := range arrays {
			check = (check*31 + numIdenticalPairs(nums) + 1) % 1000000007
		}
	}
	fmt.Printf("200 counts over 50 arrays of 200000 numbers: checksum %d\n", check)
}
