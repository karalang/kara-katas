// LeetCode #1805: Number of Different Integers in a String -- the bench in
// Go: the ★ arm over 64 random words of 1000 characters built once,
// 20000 calls.
package main

import (
	"fmt"
	"strings"
)

func numDifferentIntegers(word string) int32 {
	seen := map[string]struct{}{}
	var run strings.Builder
	inRun := false
	for _, c := range word {
		if c >= '0' && c <= '9' {
			inRun = true
			if !(run.Len() == 0 && c == '0') {
				run.WriteRune(c)
			}
		} else if inRun {
			seen[run.String()] = struct{}{}
			run = strings.Builder{}
			inRun = false
		}
	}
	if inRun {
		seen[run.String()] = struct{}{}
	}
	return int32(len(seen))
}

var seed int64 = 1805

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	words := make([]string, 64)
	for w := range words {
		var b strings.Builder
		for i := 0; i < 1000; i++ {
			if nextRandom()%2 == 0 {
				b.WriteByte(byte('0' + nextRandom()%4))
			} else {
				b.WriteByte(byte(97 + nextRandom()%26))
			}
		}
		words[w] = b.String()
	}
	var check int64
	for call := int64(0); call < 20000; call++ {
		word := words[(check+call)%64]
		check = (check*31 + int64(numDifferentIntegers(word))) % 1000000007
	}
	fmt.Printf("20000 calls over 64 words of 1000 characters: checksum %d\n", check)
}
