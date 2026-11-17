// LeetCode #2255: Count Prefixes of a Given String -- the benchmark's Go
// mirror of prefixes.kara: each word tested with strings.HasPrefix(s, w),
// the ones that hold counted.
package main

import (
	"fmt"
	"strings"
)

func countPrefixes(words []string, s string) int64 {
	var count int64
	for _, w := range words {
		if strings.HasPrefix(s, w) {
			count++
		}
	}
	return count
}

var seed int64 = 2255

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(longest, letters int64) string {
	length := nextRandom()%longest + 1
	b := make([]byte, length)
	for i := range b {
		b[i] = byte('a' + nextRandom()%letters)
	}
	return string(b)
}

func main() {
	var check int64
	for c := int64(0); c < 500; c++ {
		letters := c%5 + 1
		words := make([]string, 1000)
		for i := range words {
			words[i] = randomWord(10, letters)
		}
		s := randomWord(10, letters)
		check = (check*31 + countPrefixes(words, s) + 1) % 1000000007
	}
	fmt.Printf("500 cases of 1000 words: checksum %d\n", check)
}
