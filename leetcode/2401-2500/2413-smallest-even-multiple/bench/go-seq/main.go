// LeetCode #2413: Smallest Even Multiple -- the bench, the ★ arm in Go: n
// when n is even, and 2 n when it is odd.

package main

import "fmt"

func smallestEvenMultiple(n int64) int64 {
	if n%2 == 0 {
		return n
	}
	return 2 * n
}

func main() {
	var check int64
	for p := int64(0); p < 200000; p++ {
		for n := int64(1); n <= 150; n++ {
			check = (check*31 + smallestEvenMultiple(n) + p) % 1000000007
		}
	}
	fmt.Printf("200000 passes over n from 1 to 150: checksum %d\n", check)
}
