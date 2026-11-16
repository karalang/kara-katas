// LeetCode #1170: Compare Strings by Frequency of the Smallest Character --
// the ★ arm's bench in Go: words counted by frequency, the counts summed
// from the top down, each query answered by one look-up.
package main

import (
	"fmt"
	"strings"
)

func f(s string) int64 {
	smallest := byte('z' + 1)
	var count int64
	for i := 0; i < len(s); i++ {
		b := s[i]
		if b < smallest {
			smallest = b
			count = 1
		} else if b == smallest {
			count++
		}
	}
	return count
}

func numSmallerByFrequency(queries, words []string) []int64 {
	// above[k]: the words whose frequency is at least k
	var above [12]int64
	for _, w := range words {
		above[f(w)]++
	}
	for k := 10; k >= 0; k-- {
		above[k] += above[k+1]
	}
	out := make([]int64, len(queries))
	for i, q := range queries {
		out[i] = above[f(q)+1]
	}
	return out
}

var seed int64 = 1170

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(letters int64) string {
	n := 1 + nextRandom()%10
	var w strings.Builder
	for i := int64(0); i < n; i++ {
		w.WriteByte(byte('a' + nextRandom()%letters))
	}
	return w.String()
}

func main() {
	rounds := 300
	letters := [4]int64{2, 3, 5, 26}
	queries := make([][]string, 16)
	words := make([][]string, 16)
	for l := 0; l < 16; l++ {
		queries[l] = make([]string, 2000)
		for i := range queries[l] {
			queries[l][i] = randomWord(letters[l%4])
		}
		words[l] = make([]string, 2000)
		for i := range words[l] {
			words[l][i] = randomWord(letters[l%4])
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for l := 0; l < 16; l++ {
			i := nextRandom() % 2000
			queries[l][i] = randomWord(letters[l%4])
			j := nextRandom() % 2000
			words[l][j] = randomWord(letters[l%4])
			for _, x := range numSmallerByFrequency(queries[l], words[l]) {
				total += x
				check = (check*131 + x + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over 16 lists of 2000 queries and 2000 words: total %d, checksum %d\n", rounds, total, check)
}
