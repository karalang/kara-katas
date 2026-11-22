// LeetCode #2761: Prime Pairs With Target Sum -- the bench (primes.kara in
// Go): a sieve of Eratosthenes up to n, then each x up to n / 2 with x and
// n - x both prime.
package main

import "fmt"

func findPrimePairs(n int64) [][]int64 {
	prime := make([]bool, n+1)
	for i := range prime {
		prime[i] = true
	}
	prime[0] = false
	if n >= 1 {
		prime[1] = false
	}
	for p := int64(2); p*p <= n; p++ {
		if prime[p] {
			for m := p * p; m <= n; m += p {
				prime[m] = false
			}
		}
	}
	pairs := [][]int64{}
	for x := int64(2); x <= n/2; x++ {
		if prime[x] && prime[n-x] {
			pairs = append(pairs, []int64{x, n - x})
		}
	}
	return pairs
}

var seed int64 = 2761

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 20, 3
	targets := make([]int64, count)
	for k := range targets {
		hi := nextRandom()
		targets[k] = (hi*32768+nextRandom())%100000 + 900001
	}
	var pairsSeen, check int64
	for r := int64(0); r < rounds; r++ {
		for _, n := range targets {
			pairs := findPrimePairs(n)
			pairsSeen += int64(len(pairs))
			check = (check*31 + int64(len(pairs)) + r) % 1000000007
			for _, pair := range pairs {
				check = (check*31 + pair[0]) % 1000000007
			}
		}
	}
	fmt.Printf("%d n near 10^6, %d rounds: %d pairs, checksum %d\n", count, rounds, pairsSeen, check)
}
