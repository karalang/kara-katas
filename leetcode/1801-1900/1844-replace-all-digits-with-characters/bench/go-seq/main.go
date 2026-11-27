// LeetCode #1844: Replace All Digits with Characters -- the bench in Go: the ★ arm over
// 500000 calls on 40 strings of 100 places, built once, each call's string
// drawn from the checksum so far and one byte of its output, at a place
// drawn the same way, folded in. Each call builds its own output string.
package main

import (
	"fmt"
	"strings"
)

func replaceDigits(s string) string {
	var out strings.Builder
	for i := 0; i < len(s); i++ {
		if i%2 == 0 {
			out.WriteByte(s[i])
		} else {
			out.WriteByte(s[i-1] + s[i] - '0')
		}
	}
	return out.String()
}

func main() {
	seed := int64(1844)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	cases := make([]string, 0, 40)
	for c := 0; c < 40; c++ {
		s := make([]byte, 0, 100)
		var letter int64
		for i := 0; i < 100; i++ {
			if i%2 == 0 {
				letter = nextRandom() % 26
				s = append(s, byte('a'+letter))
			} else {
				most := min(25-letter, 9)
				s = append(s, byte('0'+nextRandom()%(most+1)))
			}
		}
		cases = append(cases, string(s))
	}
	var check int64
	for call := int64(0); call < 500000; call++ {
		out := replaceDigits(cases[(check+call)%40])
		check = (check*31 + int64(out[(check/40+call)%100])) % 1000000007
	}
	fmt.Printf("500000 calls: checksum %d\n", check)
}
