// LeetCode #2085: Count Common Words With One Occurrence -- Go mirror of
// the ★ arm's benchmark (common.kara): the same 2500 pairs of lists, the
// same count of both into a map and walk of the first.
package main

import (
	"fmt"
	"strings"
)

var seed int64 = 2085

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func counts(words []string) map[string]int64 {
	seen := map[string]int64{}
	for _, w := range words {
		seen[w]++
	}
	return seen
}

func countWords(words1, words2 []string) int64 {
	one := counts(words1)
	two := counts(words2)
	var n int64
	for w, c := range one {
		if c == 1 && two[w] == 1 {
			n++
		}
	}
	return n
}

func randomList(alphabet string, letters int64) []string {
	words := make([]string, 0, 1000)
	for i := 0; i < 1000; i++ {
		n := nextRandom()%4 + 1
		var b strings.Builder
		for j := int64(0); j < n; j++ {
			b.WriteByte(alphabet[nextRandom()%letters])
		}
		words = append(words, b.String())
	}
	return words
}

func main() {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	var total, check int64
	for t := int64(0); t < 2500; t++ {
		letters := 2 + t%25
		words1 := randomList(alphabet, letters)
		words2 := randomList(alphabet, letters)
		a := countWords(words1, words2)
		total += a
		check = (check*31 + a) % 1000000007
	}
	fmt.Printf("2500 pairs: sum %d, checksum %d\n", total, check)
}
