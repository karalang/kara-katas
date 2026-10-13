// Benchmark for #524: Go mirror of the ★ arm (check every word); see
// ../find_longest_word.kara. Like the ★ arm, every subsequence test
// copies the word's letters into a fresh slice, and a new best word is
// cloned.
package main

import (
	"fmt"
	"strings"
)

func isSubsequence(word, s string) bool {
	w := []rune(word)
	i := 0
	for _, c := range s {
		if i < len(w) && w[i] == c {
			i++
		}
	}
	return i == len(w)
}

func findLongestWord(s string, dictionary []string) string {
	best := ""
	for _, word := range dictionary {
		if len(word) > len(best) || (len(word) == len(best) && word < best) {
			if isSubsequence(word, s) {
				best = strings.Clone(word)
			}
		}
	}
	return best
}

var seed int64

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n, letters int64) string {
	b := make([]byte, 0, n)
	for i := int64(0); i < n; i++ {
		b = append(b, byte(97+nextRandom()%letters))
	}
	return string(b)
}

func randomSubsequence(s string, keep int64) string {
	b := []byte{}
	for i := 0; i < len(s); i++ {
		if nextRandom()%keep == 0 {
			b = append(b, s[i])
		}
	}
	if len(b) == 0 {
		b = append(b, s[0])
	}
	return string(b)
}

func main() {
	seed = 524
	texts := []string{}
	dictionaries := [][]string{}
	for c := 0; c < 20; c++ {
		letters := 2 + nextRandom()%4
		s := randomWord(1000, letters)
		dictionary := []string{}
		for i := 0; i < 1000; i++ {
			if nextRandom()%3 == 0 {
				keep := 2 + nextRandom()%30
				dictionary = append(dictionary, randomSubsequence(s, keep))
			} else {
				n := 1 + nextRandom()%1000
				dictionary = append(dictionary, randomWord(n, letters))
			}
		}
		texts = append(texts, s)
		dictionaries = append(dictionaries, dictionary)
	}
	total, checksum := int64(0), int64(0)
	for r := 0; r < 20; r++ {
		for c := range texts {
			answer := findLongestWord(texts[c], dictionaries[c])
			total += int64(len(answer))
			for i := 0; i < len(answer); i++ {
				checksum = (checksum*31 + int64(answer[i])) % 1000000007
			}
		}
	}
	fmt.Printf("20 cases, 20 rounds: total %d, checksum %d\n", total, checksum)
}
