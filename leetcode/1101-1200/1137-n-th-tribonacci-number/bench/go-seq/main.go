// LeetCode #1137: N-th Tribonacci Number -- the bench, the ★ arm's algorithm:
// three running values.
package main

import "fmt"

func tribonacci(n int64) int64 {
	var a, b, c int64 = 0, 1, 1
	for i := int64(0); i < n; i++ {
		next := a + b + c
		a = b
		b = c
		c = next
	}
	return a
}

var seed int64 = 1137

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var total, check int64
	for q := 0; q < 20000000; q++ {
		n := nextRandom() % 38
		t := tribonacci(n)
		total += t
		check = (check*31 + t%1000003) % 1000000007
	}
	fmt.Printf("20000000 queries, n from 0 to 37: answers total %d, checksum %d\n", total, check)
}
