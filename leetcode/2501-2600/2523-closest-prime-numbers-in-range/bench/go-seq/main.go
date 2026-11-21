// LeetCode #2523: Closest Prime Numbers in Range -- Go mirror of the
// benchmark (closest.kara): the same queries, each answered by a fresh
// sieve, and the same checksum.
package main

import "fmt"

func closestPrimes(left, right int64) (int64, int64) {
	composite := make([]bool, right+1)
	for p := int64(2); p*p <= right; p++ {
		if !composite[p] {
			for m := p * p; m <= right; m += p {
				composite[m] = true
			}
		}
	}
	a, b, last := int64(-1), int64(-1), int64(-1)
	start := left
	if start < 2 {
		start = 2
	}
	for x := start; x <= right; x++ {
		if !composite[x] {
			if last != -1 && (a == -1 || x-last < b-a) {
				a, b = last, x
			}
			last = x
		}
	}
	return a, b
}

func main() {
	const queries = 150
	var check int64
	for q := int64(0); q < queries; q++ {
		right := check%500000 + 500001
		a, b := closestPrimes(right-10000, right)
		check = (check*31 + a + q) % 1000000007
		check = (check*31 + b) % 1000000007
	}
	fmt.Printf("%d queries to 10^6: checksum %d\n", queries, check)
}
