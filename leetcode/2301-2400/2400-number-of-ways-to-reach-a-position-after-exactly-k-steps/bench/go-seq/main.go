// LeetCode #2400: Number of Ways to Reach a Position After Exactly k
// Steps -- the bench, the ★ arm in Go: C(k, (k + d) / 2) from factorials
// modulo 10^9 + 7 and Fermat's inverse.

package main

import "fmt"

const mod = 1000000007

var seed int64 = 2400

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func power(base, exponent int64) int64 {
	result, b := int64(1), base%mod
	for e := exponent; e > 0; e /= 2 {
		if e%2 == 1 {
			result = result * b % mod
		}
		b = b * b % mod
	}
	return result
}

func numberOfWays(startPos, endPos, k int64) int64 {
	d := endPos - startPos
	if d < 0 {
		d = -d
	}
	if d > k || (k-d)%2 == 1 {
		return 0
	}
	toward := (k + d) / 2
	factorial := make([]int64, k+1)
	factorial[0] = 1
	for i := int64(1); i <= k; i++ {
		factorial[i] = factorial[i-1] * i % mod
	}
	return factorial[k] * power(factorial[toward], mod-2) % mod * power(factorial[k-toward], mod-2) % mod
}

func main() {
	var check, zeros int64
	for q := 0; q < 300000; q++ {
		k := 1 + nextRandom()%1000
		start := 1 + nextRandom()%1000
		end := start - k + 2*(nextRandom()%(k+1))
		if end < 1 {
			end = 1
		}
		if end > 1000 {
			end = 1000
		}
		w := numberOfWays(start, end, k)
		if w == 0 {
			zeros++
		}
		check = (check*31 + w) % mod
	}
	fmt.Printf("300000 queries of k up to 1000: checksum %d, %d zeros\n", check, zeros)
}
