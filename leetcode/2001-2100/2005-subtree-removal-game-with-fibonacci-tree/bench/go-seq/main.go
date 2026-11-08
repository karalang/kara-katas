// LeetCode #2005: Subtree Removal Game with Fibonacci Tree -- the benchmark's
// Go twin, the same algorithm as fibtree.kara here.
package main

import "fmt"

func findGameWinner(n int64) bool {
	// value[k] is order(k)'s value; value[0] is unused
	value := make([]int64, n+1)
	for k := int64(2); k <= n; k++ {
		left := int64(0)
		if k >= 3 {
			left = value[k-2] + 1
		}
		value[k] = left ^ (value[k-1] + 1)
	}
	return value[n] != 0
}

var seed int64 = 2005

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 500000 values of n from 1 to 100 drawn once, then the ★ arm on each, 10 rounds
	queries := make([]int64, 500000)
	for i := range queries {
		queries[i] = nextRandom()%100 + 1
	}
	var calls, alice, check int64
	for r := 0; r < 10; r++ {
		for _, n := range queries {
			wins := findGameWinner(n)
			calls++
			if wins {
				alice++
			}
			add := int64(0)
			if wins {
				add = n
			}
			check = (check*31 + add) % 1000000007
		}
	}
	fmt.Printf("%d calls: Alice wins %d, checksum %d\n", calls, alice, check)
}
