// LeetCode #1249 bench, in Go: the ★ arm (a stack of the places of the `(`
// not yet closed, and a slice of flags for the characters to keep) on 50
// random strings of 100000 characters built once, each with its own share
// of parentheses, each asked 4 times; every kept string folded into a
// checksum.
package main

import (
	"fmt"
	"strings"
)

func minRemoveToMakeValid(s string) string {
	keep := make([]bool, len(s))
	open := []int{}
	for i := 0; i < len(s); i++ {
		keep[i] = true
		if s[i] == '(' {
			open = append(open, i)
		} else if s[i] == ')' {
			if len(open) == 0 {
				keep[i] = false
			} else {
				open = open[:len(open)-1]
			}
		}
	}
	for _, i := range open {
		keep[i] = false
	}
	var b strings.Builder
	for i := 0; i < len(s); i++ {
		if keep[i] {
			b.WriteByte(s[i])
		}
	}
	return b.String()
}

var seed int64 = 1249

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomText(n int, percent int64) string {
	var b strings.Builder
	for i := 0; i < n; i++ {
		if nextRandom()%100 < percent {
			if nextRandom()%2 == 0 {
				b.WriteByte('(')
			} else {
				b.WriteByte(')')
			}
		} else {
			b.WriteByte("abcde"[nextRandom()%5])
		}
	}
	return b.String()
}

func main() {
	texts := make([]string, 0, 50)
	for t := 0; t < 50; t++ {
		percent := nextRandom() % 101
		texts = append(texts, randomText(100000, percent))
	}
	var check int64
	for r := 0; r < 4; r++ {
		for _, s := range texts {
			kept := minRemoveToMakeValid(s)
			for i := 0; i < len(kept); i++ {
				check = (check*131 + int64(kept[i])) % 1000000007
			}
		}
	}
	fmt.Printf("4 rounds of 50 strings of 100000 characters: checksum %d\n", check)
}
