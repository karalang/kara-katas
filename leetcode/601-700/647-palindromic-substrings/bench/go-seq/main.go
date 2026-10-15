// LeetCode #647: Palindromic Substrings -- Go mirror of the Kāra bench.
//
// The ★ arm over the same texts and rounds: from each of the 2n - 1
// centers, the window widened while its two ends match, over the
// string's bytes.
package main

import (
	"fmt"
	"strings"
)

func countSubstrings(s string) int64 {
	n := int64(len(s))
	var count int64
	for center := int64(0); center < 2*n-1; center++ {
		lo := center / 2
		hi := lo + center%2
		for lo >= 0 && hi < n && s[lo] == s[hi] {
			count++
			lo--
			hi++
		}
	}
	return count
}

var seed int64 = 647

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const inputs = 20
	const rounds = 300
	texts := make([]string, 0, inputs)
	for i := 0; i < inputs; i++ {
		letters := 1 + nextRandom()%3
		var b strings.Builder
		for j := 0; j < 2000; j++ {
			b.WriteByte(byte(97 + nextRandom()%letters))
		}
		texts = append(texts, b.String())
	}
	var sum, checksum int64
	for r := 0; r < rounds; r++ {
		c := countSubstrings(texts[(r*7)%inputs])
		sum += c
		checksum = (checksum*31 + c) % 1000000007
	}
	fmt.Printf("%d inputs, %d rounds: total %d, checksum %d\n", inputs, rounds, sum, checksum)
}
