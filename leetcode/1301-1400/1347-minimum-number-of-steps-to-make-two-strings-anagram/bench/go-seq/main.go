// LeetCode #1347 bench -- Go: one count per letter, up for s and down for
// t, the positive counts summed.
package main

import (
	"fmt"
	"strings"
)

func minSteps(s, t string) int {
	var count [26]int
	for i := 0; i < len(s); i++ {
		count[s[i]-'a']++
	}
	for i := 0; i < len(t); i++ {
		count[t[i]-'a']--
	}
	steps := 0
	for _, c := range count {
		if c > 0 {
			steps += c
		}
	}
	return steps
}

func main() {
	var seed int64 = 1347
	var sb strings.Builder
	for i := 0; i < 1000000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		sb.WriteByte(byte('a' + (seed/65536)%26))
	}
	text := sb.String()
	var check int64
	for q := int64(0); q < 1000; q++ {
		n := 40000 + check%10001
		a := check % (1000000 - n)
		b := (check / 7) % (1000000 - n)
		steps := int64(minSteps(text[a:a+n], text[b:b+n]))
		check = (check*31 + steps + q) % 1000000007
	}
	fmt.Printf("1000 queries over a text of 10^6: checksum %d\n", check)
}
