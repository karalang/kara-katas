// LeetCode #2262: Total Appeal of A String -- Go mirror of the ★ arm
// (appeal.kara): each position counts the substrings where its letter
// first appears, (i - last) * (n - i), with the last position kept per
// letter. Output is byte-identical to appeal.kara.
package main

import (
	"fmt"
	"strings"
)

func appealSum(s string) int64 {
	n := int64(len(s))
	var last [26]int64
	for c := range last {
		last[c] = -1
	}
	var total int64
	for i := int64(0); i < n; i++ {
		c := s[i] - 'a'
		total += (i - last[c]) * (n - i)
		last[c] = i
	}
	return total
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2262

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := int64(0); t < 40; t++ {
		letters := t%26 + 1
		var b strings.Builder
		for i := 0; i < 100000; i++ {
			b.WriteByte(byte('a' + nextRandom()%letters))
		}
		check = (check*31 + appealSum(b.String())) % 1000000007
	}
	fmt.Printf("40 strings of 10^5: checksum %d\n", check)
}
