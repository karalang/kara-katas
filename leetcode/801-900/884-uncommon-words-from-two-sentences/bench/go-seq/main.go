// LeetCode #884 bench: Go mirror of uncommon_from_sentences.kara (the ★
// arm, one map of counts) on the same 1000 sentences.
package main

import (
	"fmt"
	"strings"
)

func uncommonFromSentences(s1, s2 string) []string {
	counts := map[string]int64{}
	for _, word := range strings.Split(s1, " ") {
		counts[word] = counts[word] + 1
	}
	for _, word := range strings.Split(s2, " ") {
		counts[word] = counts[word] + 1
	}
	out := []string{}
	for word, n := range counts {
		if n == 1 {
			out = append(out, word)
		}
	}
	return out
}

var seed int64 = 884

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// up to 200 characters, words of 1 to 4 of the letters a to e
func sentence() string {
	out := ""
	for {
		size := nextRandom()%4 + 1
		word := ""
		for k := int64(0); k < size; k++ {
			word += string(rune(97 + nextRandom()%5))
		}
		if len(out) == 0 {
			out = word
		} else if len(out)+1+len(word) <= 200 {
			out = out + " " + word
		} else {
			return out
		}
		if nextRandom()%80 == 0 {
			return out
		}
	}
}

// the same for a word wherever it sits in the answer
func wordHash(word string) int64 {
	var h int64 = 7
	for k := 0; k < len(word); k++ {
		h = (h*131 + int64(word[k])) % 1000000007
	}
	return h
}

func main() {
	sentences := make([]string, 1000)
	for i := range sentences {
		sentences[i] = sentence()
	}
	var total, check int64
	for r := 0; r < 200; r++ {
		for i := 0; i < 1000; i++ {
			words := uncommonFromSentences(sentences[i], sentences[(i+r+1)%1000])
			total += int64(len(words))
			for _, w := range words {
				check = (check + wordHash(w)) % 1000000007
			}
		}
	}
	fmt.Printf("1000 sentences, each paired with 200 others: %d uncommon words, checksum %d\n", total, check)
}
