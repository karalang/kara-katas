// LeetCode #2278: Percentage of Letter in String -- the bench, the ★ arm.
package main

import (
	"fmt"
	"strings"
)

func percentageLetter(s string, letter rune) int64 {
	var count int64
	for _, c := range s {
		if c == letter {
			count++
		}
	}
	return count * 100 / int64(len(s))
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2278

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 100000; t++ {
		var b strings.Builder
		for i := 0; i < 100; i++ {
			b.WriteByte(byte('a' + nextRandom()%4))
		}
		letter := rune('a' + nextRandom()%4)
		check = (check*31 + percentageLetter(b.String(), letter)) % 1000000007
	}
	fmt.Printf("100000 strings of 100: checksum %d\n", check)
}
