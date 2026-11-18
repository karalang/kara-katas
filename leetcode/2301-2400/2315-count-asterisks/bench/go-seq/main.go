// LeetCode #2315: Count Asterisks -- the bench, the ★ arm in Go. One
// pass with a flag: each `|` flips whether the walk is inside a pair,
// and a `*` counts only outside one.
package main

import (
	"fmt"
	"strings"
)

func countAsterisks(s string) int64 {
	inside := false
	var count int64
	for _, c := range s {
		if c == '|' {
			inside = !inside
		} else if c == '*' && !inside {
			count++
		}
	}
	return count
}

var seed int64 = 2315

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strs := make([]string, 0, 1000)
	for a := 0; a < 1000; a++ {
		bars := nextRandom()%8 + 2
		var b strings.Builder
		count := 0
		for i := 0; i < 999; i++ {
			if nextRandom()%bars == 0 {
				b.WriteByte('|')
				count++
			} else if nextRandom()%2 == 0 {
				b.WriteByte('*')
			} else {
				b.WriteByte('a')
			}
		}
		if count%2 == 1 {
			b.WriteByte('|')
		} else {
			b.WriteByte('a')
		}
		strs = append(strs, b.String())
	}
	var check int64
	for p := 0; p < 100; p++ {
		for a := 0; a < 1000; a++ {
			check = (check*31 + countAsterisks(strs[(7*a+p)%1000])) % 1000000007
		}
	}
	fmt.Printf("100 passes over 1000 strings of 1000 characters: checksum %d\n", check)
}
