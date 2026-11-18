// LeetCode #1190 bench: the ★ arm in Go, over the same 200 strings of about
// 2000 characters and 200 rounds as the Kāra bench.
package main

import (
	"fmt"
	"strings"
)

func reverseParentheses(s string) string {
	n := len(s)
	pair := make([]int, n)
	open := make([]int, 0)
	for i := 0; i < n; i++ {
		if s[i] == '(' {
			open = append(open, i)
		} else if s[i] == ')' {
			j := open[len(open)-1]
			open = open[:len(open)-1]
			pair[i] = j
			pair[j] = i
		}
	}
	var out strings.Builder
	out.Grow(n)
	i, step := 0, 1
	for i < n {
		c := s[i]
		if c == '(' || c == ')' {
			i = pair[i]
			step = -step
		} else {
			out.WriteByte(c)
		}
		i += step
	}
	return out.String()
}

var seed int64 = 1190

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

const letters = "abcdefghijklmnopqrstuvwxyz"

func randomCase(n int) string {
	var s strings.Builder
	open := 0
	for k := 0; k < n; k++ {
		r := nextRandom() % 4
		if r == 0 {
			s.WriteByte('(')
			open++
		} else if r == 1 && open > 0 {
			s.WriteByte(')')
			open--
		} else {
			s.WriteByte(letters[nextRandom()%26])
		}
	}
	for k := 0; k < open; k++ {
		s.WriteByte(')')
	}
	return s.String()
}

func nested(depth int) string {
	var s strings.Builder
	for k := 0; k < depth; k++ {
		s.WriteByte(letters[nextRandom()%26])
		s.WriteByte('(')
	}
	for k := 0; k < depth; k++ {
		s.WriteByte(letters[nextRandom()%26])
		s.WriteByte(')')
	}
	return s.String()
}

func digest(s string) int64 {
	var h int64
	for i := 0; i < len(s); i++ {
		h = (h*131 + int64(s[i])) % 1000000007
	}
	return h
}

func main() {
	cases := make([]string, 200)
	for i := range cases {
		if i%2 == 0 {
			cases[i] = randomCase(2000)
		} else {
			cases[i] = nested(500)
		}
	}
	var check int64
	for r := 0; r < 200; r++ {
		for _, s := range cases {
			check = (check*131 + digest(reverseParentheses(s))) % 1000000007
		}
	}
	fmt.Printf("200 rounds of 200 strings of about 2000 characters: checksum %d\n", check)
}
