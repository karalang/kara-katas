// LeetCode #1830: Minimum Number of Operations to Make String Sorted -- the
// bench in Go: the ★ arm over 500 calls on runs of 1500 to 2999 letters cut
// from one string of 4500 random letters, built once, each run's start and
// length drawn from the checksum so far. Each call makes its run a string of
// its own.
package main

import "fmt"

const mod = 1000000007

func power(base, exp int64) int64 {
	result, b, e := int64(1), base%mod, exp
	for e > 0 {
		if e%2 == 1 {
			result = result * b % mod
		}
		b = b * b % mod
		e /= 2
	}
	return result
}

func makeStringSorted(s string) int64 {
	n := int64(len(s))
	fact := make([]int64, n+1)
	fact[0] = 1
	for i := int64(1); i <= n; i++ {
		fact[i] = fact[i-1] * i % mod
	}
	inverse := make([]int64, n+1)
	inverse[n] = power(fact[n], mod-2)
	for i := n - 1; i >= 0; i-- {
		inverse[i] = inverse[i+1] * (i + 1) % mod
	}
	var count [26]int64
	var operations int64
	for i := n - 1; i >= 0; i-- {
		c := int64(s[i] - 'a')
		count[c]++
		var smaller int64
		for _, k := range count[:c] {
			smaller += k
		}
		ways := fact[n-1-i] * smaller % mod
		for _, k := range count {
			ways = ways * inverse[k] % mod
		}
		operations = (operations + ways) % mod
	}
	return operations
}

var seed int64 = 1830

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := make([]byte, 4500)
	for i := range letters {
		letters[i] = byte('a' + nextRandom()%26)
	}
	var check int64
	for call := int64(0); call < 500; call++ {
		start := (check + call) % 1500
		length := 1500 + (check*7+call)%1500
		s := string(letters[start : start+length])
		check = (check*31 + makeStringSorted(s)) % 1000000007
	}
	fmt.Printf("500 calls: checksum %d\n", check)
}
