// LeetCode #1015: Smallest Integer Divisible by K -- bench
// Mirrors ../repunit.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

func smallestRepunitDivByK(k int64) int64 {
	if k%2 == 0 || k%5 == 0 {
		return -1
	}
	var r int64
	for length := int64(1); length < k+1; length++ {
		r = (r*10 + 1) % k
		if r == 0 {
			return length
		}
	}
	return -1
}

func main() {
	last := int64(30000)
	var none, total, check int64
	for k := int64(1); k < last+1; k++ {
		answer := smallestRepunitDivByK(k)
		if answer < 0 {
			none++
		} else {
			total += answer
		}
		check = (check*31 + answer + 1) % 1000000007
	}
	fmt.Printf("k = 1..%d: %d with no answer, the rest sum to %d, checksum %d\n", last, none, total, check)
}
