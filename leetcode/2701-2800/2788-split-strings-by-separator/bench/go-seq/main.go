// LeetCode #2788: Split Strings by Separator -- the bench in Go: the ★ arm
// over 20000 lists of 100 words of 20 characters from a, b, c and the six
// separators, each split by one of them, all drawn first, then each
// answered 10 times.
package main

import (
	"fmt"
	"strings"
)

func splitWordsBySeparator(words []string, separator byte) []string {
	var out []string
	sep := string(separator)
	for _, w := range words {
		for _, piece := range strings.Split(w, sep) {
			if piece != "" {
				out = append(out, strings.Clone(piece))
			}
		}
	}
	return out
}

var seed int64 = 2788

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type kase struct {
	words     []string
	separator byte
}

func main() {
	count := 20000
	rounds := 10
	letters := "abc.,|$#@"
	separators := ".,|$#@"
	cases := make([]kase, 0, count)
	for c := 0; c < count; c++ {
		words := make([]string, 100)
		for k := range words {
			b := make([]byte, 20)
			for i := range b {
				b[i] = letters[nextRandom()%9]
			}
			words[k] = string(b)
		}
		cases = append(cases, kase{words, separators[nextRandom()%6]})
	}
	var pieces, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, k := range cases {
			got := splitWordsBySeparator(k.words, k.separator)
			pieces += int64(len(got))
			for _, p := range got {
				check = (check*31 + int64(len(p)) + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d lists of 100 words, %d rounds: %d pieces, checksum %d\n", count, rounds, pieces, check)
}
