// LeetCode #1175: Prime Arrangements -- the ★ arm's bench in Go: a sieve
// of Eratosthenes over a []bool counts the primes up to n, and the answer
// is p! * (n - p)! modulo 10^9 + 7. The same million calls.
package main

import "fmt"

const MOD = 1000000007

func factorial(k int64) int64 {
	f := int64(1)
	for i := int64(2); i <= k; i++ {
		f = f * i % MOD
	}
	return f
}

func numPrimeArrangements(n int64) int64 {
	composite := make([]bool, n+1)
	var primes int64
	for i := int64(2); i <= n; i++ {
		if !composite[i] {
			primes++
			for j := i * i; j <= n; j += i {
				composite[j] = true
			}
		}
	}
	return factorial(primes) * factorial(n-primes) % MOD
}

var seed int64 = 1175

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	calls := 1000000
	var check int64
	for c := 0; c < calls; c++ {
		n := 1 + nextRandom()%100
		check = (check*131 + numPrimeArrangements(n)) % 1000000007
	}
	fmt.Printf("%d calls: checksum %d\n", calls, check)
}
