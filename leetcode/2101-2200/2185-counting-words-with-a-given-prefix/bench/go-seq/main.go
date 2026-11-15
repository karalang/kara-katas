// LeetCode #2185: Counting Words With a Given Prefix -- the benchmark's
// Go mirror of prefix_count.kara: each word asked whether it has the
// prefix, by strings.HasPrefix.
package main

import (
	"fmt"
	"strings"
)

func prefixCount(words []string, pref string) int64 {
	var count int64
	for _, w := range words {
		if strings.HasPrefix(w, pref) {
			count++
		}
	}
	return count
}

var seed int64 = 2185

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte(97 + nextRandom()%2)
	}
	return string(b)
}

func main() {
	words := make([]string, 0, 100)
	for i := 0; i < 100; i++ {
		length := nextRandom()%100 + 1
		words = append(words, randomWord(length))
	}
	var check int64
	for r := 0; r < 100000; r++ {
		length := nextRandom()%8 + 1
		pref := randomWord(length)
		check = (check*31 + prefixCount(words, pref)) % 1000000007
	}
	fmt.Printf("100000 solves: checksum %d\n", check)
}
