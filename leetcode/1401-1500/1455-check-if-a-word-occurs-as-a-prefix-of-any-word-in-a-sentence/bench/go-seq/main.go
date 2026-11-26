// LeetCode #1455 bench mirror: the first word that starts with the search
// word, counted from 1.
package main

import (
	"fmt"
	"strings"
)

func isPrefixOfWord(sentence, searchWord string) int32 {
	for i, w := range strings.Split(sentence, " ") {
		if strings.HasPrefix(w, searchWord) {
			return int32(i) + 1
		}
	}
	return -1
}

var seed int64 = 1455

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// a word of 1 to `longest` letters drawn from the first 4 of the alphabet
func word(longest int64) string {
	n := 1 + nextRandom()%longest
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom()%4)
	}
	return string(b)
}

func main() {
	// 2000 sentences of 100 letters of words of 1 to 8 letters and 2000
	// search words of 1 to 4 letters, drawn once, then every search word
	// looked for in every sentence, the answers folded to a checksum
	sentences := make([]string, 0, 2000)
	for i := 0; i < 2000; i++ {
		s := word(8)
		for {
			w := word(8)
			if len(s)+1+len(w) > 100 {
				break
			}
			s += " " + w
		}
		sentences = append(sentences, s)
	}
	searches := make([]string, 2000)
	for i := range searches {
		searches[i] = word(4)
	}
	var check int64
	for _, s := range sentences {
		for _, w := range searches {
			check = (check*131 + int64(isPrefixOfWord(s, w)) + 1) % 1000000007
		}
	}
	fmt.Printf("4 x 10^6 searches: checksum %d\n", check)
}
