// LeetCode #1576: Replace All ?'s to Avoid Consecutive Repeating
// Characters -- bench: the ★ arm (the first of a, b, c that fits, in a
// Vec[char]) over 20 strings of 500000 characters, half of them '?', built
// once; then 4 rounds answering all 20, each answer folded to its count of
// 'a's.
package main

import (
	"fmt"
	"strings"
)

func modifyString(s string) string {
	cs := []rune(s)
	n := len(cs)
	for i := 0; i < n; i++ {
		if cs[i] == '?' {
			for _, c := range []rune{'a', 'b', 'c'} {
				if (i == 0 || cs[i-1] != c) && (i+1 == n || cs[i+1] != c) {
					cs[i] = c
					break
				}
			}
		}
	}
	return string(cs)
}

var seed int64 = 1576

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 500000
	strs := make([]string, 0, 20)
	for v := 0; v < 20; v++ {
		var b strings.Builder
		last := ' '
		for i := 0; i < n; i++ {
			if nextRandom()%2 == 0 {
				b.WriteByte('?')
				last = '?'
			} else {
				k := nextRandom() % 26
				if rune('a'+k) == last {
					k = (k + 1) % 26
				}
				c := rune('a' + k)
				b.WriteRune(c)
				last = c
			}
		}
		strs = append(strs, b.String())
	}
	var check, total int64
	for r := 0; r < 4; r++ {
		for _, s := range strs {
			a := int64(strings.Count(modifyString(s), "a"))
			total += a
			check = mix(check, a)
		}
	}
	fmt.Printf("80 answers over 20 strings of %d characters: 'a' total %d, checksum %d\n", n, total, check)
}
