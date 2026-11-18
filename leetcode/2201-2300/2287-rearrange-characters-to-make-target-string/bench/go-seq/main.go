// LeetCode #2287: Rearrange Characters to Make Target String -- the
// bench, the ★ arm's Go twin. Two arrays of 26 counts and the least
// quotient.
package main

import (
	"fmt"
	"strings"
)

func rearrangeCharacters(s, target string) int64 {
	var have, need [26]int64
	for i := 0; i < len(s); i++ {
		have[s[i]-'a']++
	}
	for i := 0; i < len(target); i++ {
		need[target[i]-'a']++
	}
	copies := int64(len(s))
	for i := 0; i < 26; i++ {
		if need[i] > 0 {
			copies = min(copies, have[i]/need[i])
		}
	}
	return copies
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2287

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func word(n, letters int64) string {
	var b strings.Builder
	for i := int64(0); i < n; i++ {
		b.WriteByte(byte('a' + nextRandom()%letters))
	}
	return b.String()
}

func main() {
	type pair struct{ s, target string }
	pairs := make([]pair, 0, 10000)
	for i := 0; i < 10000; i++ {
		letters := nextRandom()%6 + 1
		sLen := nextRandom()%100 + 1
		tLen := nextRandom()%10 + 1
		s := word(sLen, letters)
		target := word(tLen, letters)
		pairs = append(pairs, pair{s, target})
	}
	var check int64
	for p := 0; p < 200; p++ {
		var total int64
		for _, q := range pairs {
			total += rearrangeCharacters(q.s, q.target)
		}
		check = (check*31 + total) % 1000000007
	}
	fmt.Printf("200 passes over 10^4 pairs: checksum %d\n", check)
}
