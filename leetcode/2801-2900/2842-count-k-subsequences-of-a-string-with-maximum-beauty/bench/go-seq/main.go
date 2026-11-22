// LeetCode #2842: Count K-Subsequences of a String With Maximum Beauty
// -- the bench, mirrored from beauty.kara: the counts sorted, most
// first, the letters above the k-th all taken and the rest chosen
// among those tied with it.
package main

import (
	"fmt"
	"sort"
)

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

func choose(n, r int64) int64 {
	top, bottom := int64(1), int64(1)
	for i := int64(0); i < r; i++ {
		top = top * (n - i) % mod
		bottom = bottom * (i + 1) % mod
	}
	return top * power(bottom, mod-2) % mod
}

func countKSubsequencesWithMaxBeauty(s string, k int64) int64 {
	count := make([]int64, 26)
	for i := 0; i < len(s); i++ {
		count[s[i]-'a']++
	}
	freq := []int64{}
	for _, c := range count {
		if c > 0 {
			freq = append(freq, c)
		}
	}
	if k > int64(len(freq)) {
		return 0
	}
	sort.Slice(freq, func(a, b int) bool { return freq[a] > freq[b] })
	last := freq[k-1]
	var above, tied int64
	for _, f := range freq {
		if f > last {
			above++
		}
		if f == last {
			tied++
		}
	}
	ways := choose(tied, k-above) * power(last, k-above) % mod
	for _, f := range freq[:above] {
		ways = ways * f % mod
	}
	return ways
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, n, rounds = 100, 200000, 40
	seed := int64(2842)
	type caseT struct {
		s string
		k int64
	}
	cases := make([]caseT, 0, count)
	for c := 0; c < count; c++ {
		kinds := nextRandom(&seed)%24 + 3
		codes := make([]byte, n)
		for i := range codes {
			codes[i] = byte(97 + nextRandom(&seed)%kinds)
		}
		k := nextRandom(&seed)%26 + 1
		cases = append(cases, caseT{string(codes), k})
	}
	var zero, check int64
	for r := int64(0); r < rounds; r++ {
		for _, cs := range cases {
			ways := countKSubsequencesWithMaxBeauty(cs.s, cs.k)
			if ways == 0 {
				zero++
			}
			check = (check*31 + ways + r) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d, %d rounds: %d with none, checksum %d\n", count, n, rounds, zero, check)
}
