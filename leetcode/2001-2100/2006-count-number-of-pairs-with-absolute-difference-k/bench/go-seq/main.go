// LeetCode #2006: Count Number of Pairs With Absolute Difference K -- the
// benchmark's Go twin, the same algorithm as pairs.kara here.
package main

import "fmt"

func countKDifference(nums []int64, k int64) int64 {
	seen := make([]int64, 101)
	var pairs int64
	for _, x := range nums {
		if x-k >= 1 {
			pairs += seen[x-k]
		}
		if x+k <= 100 {
			pairs += seen[x+k]
		}
		seen[x]++
	}
	return pairs
}

var seed int64 = 2006

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20000 arrays of 200 values up to 100 built once, then the ★ arm on
	// each for 25 rounds, k moving with the round
	arrays := make([][]int64, 20000)
	for a := range arrays {
		arrays[a] = make([]int64, 200)
		for i := range arrays[a] {
			arrays[a][i] = nextRandom()%100 + 1
		}
	}
	var calls, sum, check int64
	for r := int64(0); r < 25; r++ {
		for a := range arrays {
			k := (r*37+int64(a))%99 + 1
			answer := countKDifference(arrays[a], k)
			calls++
			sum += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
