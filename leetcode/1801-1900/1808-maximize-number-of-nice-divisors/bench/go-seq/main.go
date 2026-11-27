// LeetCode #1808: Maximize Number of Nice Divisors -- the bench in Go: the
// ★ arm over 2 * 10^6 calls, each count of prime factors drawn from the
// checksum so far.
package main

import "fmt"

const mod = 1000000007

func power(base, exp int64) int64 {
	result := int64(1)
	b := base % mod
	e := exp
	for e > 0 {
		if e%2 == 1 {
			result = result * b % mod
		}
		b = b * b % mod
		e /= 2
	}
	return result
}

func maxNiceDivisors(primeFactors int32) int32 {
	n := int64(primeFactors)
	if n <= 3 {
		return primeFactors
	}
	var answer int64
	switch n % 3 {
	case 0:
		answer = power(3, n/3)
	case 1:
		answer = power(3, n/3-1) * 4 % mod
	default:
		answer = power(3, n/3) * 2 % mod
	}
	return int32(answer)
}

func main() {
	var check int64
	for call := int64(0); call < 2000000; call++ {
		n := 1 + (check*7919+call)%1000000000
		check = (check*31 + int64(maxNiceDivisors(int32(n)))) % 1000000007
	}
	fmt.Printf("2000000 calls: checksum %d\n", check)
}
