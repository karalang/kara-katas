// LeetCode #1119: Remove Vowels from a String -- the bench in Go, the ★
// arm's filter over the same 64 texts and 2000 rounds.
package main

import (
	"fmt"
	"strings"
)

func removeVowels(s string) string {
	var b strings.Builder
	for _, c := range s {
		switch c {
		case 'a', 'e', 'i', 'o', 'u':
		default:
			b.WriteRune(c)
		}
	}
	return b.String()
}

var seed int64 = 1119

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := []rune("abcdefghijklmnopqrstuvwxyz")
	texts := make([][]rune, 64)
	for j := range texts {
		texts[j] = make([]rune, 1000)
		for i := range texts[j] {
			texts[j][i] = letters[nextRandom()%26]
		}
	}
	var kept, check int64
	for round := 0; round < 2000; round++ {
		for j := range texts {
			at := (round*7919 + j*104729) % 1000
			texts[j][at] = letters[(round+j)%26]
			r := removeVowels(string(texts[j]))
			kept += int64(len(r))
			first := int64(0)
			if len(r) > 0 {
				first = int64(r[0])
			}
			check = (check*31 + int64(len(r)) + first) % 1000000007
		}
	}
	fmt.Printf("2000 rounds over 64 texts of 1000 letters: %d letters kept, checksum %d\n", kept, check)
}
