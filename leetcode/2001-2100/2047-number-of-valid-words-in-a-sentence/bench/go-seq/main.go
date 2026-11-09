// LeetCode #2047 -- the ★ arm as a benchmark; mirror of ../valid.kara: each
// token's runes collected into a slice, as the Kāra arm does.
package main

import (
	"fmt"
	"strings"
)

func isLower(c rune) bool { return c >= 'a' && c <= 'z' }

func isValid(token string) bool {
	cs := []rune(token)
	n := len(cs)
	hyphens := 0
	for i := 0; i < n; i++ {
		c := cs[i]
		if c >= '0' && c <= '9' {
			return false
		}
		if c == '-' {
			hyphens++
			if hyphens > 1 || i == 0 || i == n-1 {
				return false
			}
			if !isLower(cs[i-1]) || !isLower(cs[i+1]) {
				return false
			}
		}
		if (c == '!' || c == '.' || c == ',') && i != n-1 {
			return false
		}
	}
	return true
}

func countValidWords(sentence string) int64 {
	var count int64
	for _, token := range strings.Fields(sentence) {
		if isValid(token) {
			count++
		}
	}
	return count
}

var seed int64 = 2047

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	symbols := []rune("abcdefgh--!.,9")
	sentences := make([]string, 0, 2000)
	for k := 0; k < 2000; k++ {
		var b strings.Builder
		for j := 0; j < 1000; j++ {
			r := nextRandom() % 100
			if r < 70 {
				b.WriteRune(symbols[nextRandom()%8])
			} else if r < 85 {
				b.WriteRune(' ')
			} else {
				b.WriteRune(symbols[nextRandom()%int64(len(symbols))])
			}
		}
		sentences = append(sentences, b.String())
	}
	var calls, words, check int64
	for r := 0; r < 100; r++ {
		for _, s := range sentences {
			n := countValidWords(s[r%7:])
			calls++
			words += n
			check = (check*31 + n) % 1000000007
		}
	}
	fmt.Printf("%d calls: %d valid words, checksum %d\n", calls, words, check)
}
