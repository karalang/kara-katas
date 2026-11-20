// LeetCode #2341: Maximum Number of Pairs in Array -- the bench, the ★ arm
// in Go: each value counted in a table of 101, the pairs every count's
// half and the leftovers its parity.
package main

import "fmt"

func numberOfPairs(nums []int64) []int64 {
	counts := make([]int64, 101)
	for _, x := range nums {
		counts[x]++
	}
	pairs, left := int64(0), int64(0)
	for _, c := range counts {
		pairs += c / 2
		left += c % 2
	}
	return []int64{pairs, left}
}

func scrambled(index int64) int64 {
	return index * 2654435761 % 2147483647
}

func main() {
	arrays := make([][]int64, 10)
	for a := int64(0); a < 10; a++ {
		arrays[a] = make([]int64, 100000)
		for i := int64(0); i < 100000; i++ {
			arrays[a][i] = scrambled(a*100000+i) % 101
		}
	}
	check := int64(0)
	for p := int64(0); p < 50; p++ {
		for _, nums := range arrays {
			answer := numberOfPairs(nums)
			check = (check*31 + answer[0]*101 + answer[1] + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
