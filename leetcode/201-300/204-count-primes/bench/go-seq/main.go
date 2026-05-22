// LeetCode 204 — Go single-threaded mirror. Idiomatic for-loop +
// `append` over `[0, n)`. Same sink as the other seq-lane mirrors
// (kara, rust, c) for N = 10_000_000.
package main

import "fmt"

func isPrime(n int64) bool {
	if n < 2 {
		return false
	}
	if n == 2 {
		return true
	}
	if n%2 == 0 {
		return false
	}
	for i := int64(3); i*i <= n; i += 2 {
		if n%i == 0 {
			return false
		}
	}
	return true
}

func main() {
	const n int64 = 10_000_000

	primes := make([]int64, 0)
	for k := int64(0); k < n; k++ {
		if isPrime(k) {
			primes = append(primes, k)
		}
	}

	var sum int64
	for _, p := range primes {
		sum += p
	}
	fmt.Println(len(primes))
	fmt.Println(sum)
}
