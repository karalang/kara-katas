// LeetCode 758 — Bold Words in String: benchmark, the ★ arm in Go.
package main

import (
	"fmt"
	"strings"
)

func boldWords(words []string, s string) string {
	n := len(s)
	bold := make([]bool, n)
	for _, word := range words {
		from := 0
		for from < n {
			at := strings.Index(s[from:], word)
			if at < 0 {
				break
			}
			for i := from + at; i < from+at+len(word); i++ {
				bold[i] = true
			}
			from = from + at + 1
		}
	}
	var out strings.Builder
	for i := 0; i < n; i++ {
		if bold[i] && (i == 0 || !bold[i-1]) {
			out.WriteString("<b>")
		}
		out.WriteByte(s[i])
		if bold[i] && (i == n-1 || !bold[i+1]) {
			out.WriteString("</b>")
		}
	}
	return out.String()
}

var seed int64 = 758

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomText(length, letters int64) string {
	b := make([]byte, length)
	for i := range b {
		b[i] = byte('a' + nextRandom()%letters)
	}
	return string(b)
}

func main() {
	rounds := 20000
	total := int64(0)
	check := int64(0)
	for r := 0; r < rounds; r++ {
		s := randomText(500, 4)
		words := []string{}
		for w := 0; w < 50; w++ {
			size := 1 + nextRandom()%10
			words = append(words, randomText(size, 5))
		}
		answer := boldWords(words, s)
		total += int64(len(answer))
		for i := 0; i < len(answer); i++ {
			check = (check*31 + int64(answer[i])) % 1000000007
		}
	}
	fmt.Printf("%d strings of 500 letters: %d characters out, checksum %d\n", rounds, total, check)
}
