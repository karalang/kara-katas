// LeetCode #1021: Remove Outermost Parentheses -- bench
// Mirrors ../remove_outer.kara; see ../../README.md § Benchmarks.
package main

import (
	"fmt"
	"strings"
)

func removeOuterParentheses(s string) string {
	var out strings.Builder
	depth := 0
	for _, c := range s {
		if c == '(' {
			if depth > 0 {
				out.WriteRune(c)
			}
			depth++
		} else {
			depth--
			if depth > 0 {
				out.WriteRune(c)
			}
		}
	}
	return out.String()
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 100, 30
	seed := int64(1021)
	strs := []string{}
	chars := 0
	for g := 0; g < count; g++ {
		pairs := (nextRandom(&seed)*32768+nextRandom(&seed))%50000 + 1
		open := 2 + nextRandom(&seed)%5
		var s strings.Builder
		left := pairs
		depth := 0
		for left > 0 || depth > 0 {
			var opens bool
			if depth == 0 {
				opens = true
			} else if left == 0 {
				opens = false
			} else {
				opens = nextRandom(&seed)%8 < open
			}
			if opens {
				s.WriteByte('(')
				left--
				depth++
			} else {
				s.WriteByte(')')
				depth--
			}
		}
		chars += s.Len()
		strs = append(strs, s.String())
	}
	var kept, check int64
	for r := 0; r < rounds; r++ {
		for _, s := range strs {
			answer := removeOuterParentheses(s)
			n := int64(len(answer))
			var middle int64
			if n > 0 {
				middle = int64(answer[n/2])
			}
			kept += n
			check = (check*31 + n*2 + middle) % 1000000007
		}
	}
	fmt.Printf("%d strings, %d characters, %d rounds: %d kept, checksum %d\n", count, chars, rounds, kept, check)
}
