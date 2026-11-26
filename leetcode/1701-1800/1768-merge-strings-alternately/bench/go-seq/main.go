// LeetCode #1768: Merge Strings Alternately -- the bench in Go, mirroring
// merge_alternately.kara: the words' letters as rune slices, one index
// walking both into a strings.Builder.
package main

import (
	"fmt"
	"strings"
)

func mergeAlternately(word1, word2 string) string {
	a, b := []rune(word1), []rune(word2)
	var merged strings.Builder
	for i := 0; i < max(len(a), len(b)); i++ {
		if i < len(a) {
			merged.WriteRune(a[i])
		}
		if i < len(b) {
			merged.WriteRune(b[i])
		}
	}
	return merged.String()
}

var seed int64 = 1768

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	words := make([]string, 1000)
	for w := range words {
		n := 1 + nextRandom()%100
		b := make([]byte, n)
		for i := range b {
			b[i] = byte(97 + nextRandom()%26)
		}
		words[w] = string(b)
	}
	var check int64
	for call := int64(0); call < 2000000; call++ {
		a := (check + call*7919) % 1000
		b := (check/3 + call*104729) % 1000
		merged := mergeAlternately(words[a], words[b])
		at := check % int64(len(merged))
		check = (check*31 + int64(len(merged)) + int64(merged[at])) % 1000000007
	}
	fmt.Printf("2000000 calls over 1000 words: checksum %d\n", check)
}
