// LeetCode #1621: Number of Sets of K Non-Overlapping Line Segments -- the
// bench in Go, mirroring segments.kara: C(n + k - 1, 2k) by factorials and
// Fermat's inverse, the factorials made afresh for every query.
package main

import "fmt"

const mod int64 = 1000000007

func power(base, exp int64) int64 {
	result, b, e := int64(1), base%mod, exp
	for e > 0 {
		if e&1 == 1 {
			result = result * b % mod
		}
		b = b * b % mod
		e >>= 1
	}
	return result
}

func numberOfSets(n, k int32) int32 {
	top := int64(n) + int64(k) - 1
	pick := 2 * int64(k)
	fact := make([]int64, top+1)
	fact[0] = 1
	for i := int64(1); i <= top; i++ {
		fact[i] = fact[i-1] * i % mod
	}
	below := fact[pick] * fact[top-pick] % mod
	return int32(fact[top] * power(below, mod-2) % mod)
}

var seed int64 = 1621

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type pair struct{ n, k int32 }
	pairs := make([]pair, 400000)
	for i := range pairs {
		n := int32(nextRandom()%999 + 2)
		k := int32(nextRandom()%int64(n-1) + 1)
		pairs[i] = pair{n, k}
	}
	var check, total int64
	for _, p := range pairs {
		ways := int64(numberOfSets(p.n, p.k))
		total = (total + ways) % mod
		check = (check*31 + ways + 1) % 1000000007
	}
	fmt.Printf("400000 random pairs: counts sum to %d mod 10^9 + 7, checksum %d\n", total, check)
}
