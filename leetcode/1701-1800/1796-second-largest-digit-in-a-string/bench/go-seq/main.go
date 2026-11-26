// LeetCode #1796: Second Largest Digit in a String -- the bench in Go: the ★
// arm over 1000 random strings of 100 characters built once, 1000000 calls.
package main

import (
	"fmt"
	"strings"
)

func secondHighest(s string) int32 {
	first, second := int32(-1), int32(-1)
	for _, c := range s {
		if c >= '0' && c <= '9' {
			d := int32(c - '0')
			if d > first {
				second = first
				first = d
			} else if d < first && d > second {
				second = d
			}
		}
	}
	return second
}

var seed int64 = 1796

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	texts := make([]string, 0, 1000)
	for t := 0; t < 1000; t++ {
		digits := 1 + nextRandom()%9
		var b strings.Builder
		for x := 0; x < 100; x++ {
			if nextRandom()%10 < digits {
				b.WriteByte(byte('0' + nextRandom()%10))
			} else {
				b.WriteByte("abcdef"[nextRandom()%6])
			}
		}
		texts = append(texts, b.String())
	}
	var check int64
	for call := int64(0); call < 1000000; call++ {
		check = (check*31 + int64(secondHighest(texts[(check+call)%1000])) + 1) % 1000000007
	}
	fmt.Printf("1000000 calls over 1000 strings: checksum %d\n", check)
}
