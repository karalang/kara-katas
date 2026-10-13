// Benchmark for #527: Go mirror of the ★ arm (grow clashing prefixes);
// see ../words_abbreviation.kara. Like the ★ arm, every abbreviation is
// a fresh string and each round of growing builds a fresh clash slice.
package main

import (
	"fmt"
	"strconv"
)

func abbreviate(word string, k int) string {
	n := len(word)
	if k >= n-2 {
		return string([]byte(word))
	}
	return word[:k] + strconv.Itoa(n-1-k) + word[n-1:]
}

func wordsAbbreviation(words []string) []string {
	n := len(words)
	prefix := make([]int, n)
	abbr := make([]string, n)
	for i, w := range words {
		prefix[i] = 1
		abbr[i] = abbreviate(w, 1)
	}
	for i := 0; i < n; i++ {
		for {
			clash := []int{}
			for j := i + 1; j < n; j++ {
				if abbr[j] == abbr[i] {
					clash = append(clash, j)
				}
			}
			if len(clash) == 0 {
				break
			}
			clash = append(clash, i)
			for _, j := range clash {
				prefix[j]++
				abbr[j] = abbreviate(words[j], prefix[j])
			}
		}
	}
	return abbr
}

var seed int64 = 527

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n, letters int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte(97 + nextRandom()%letters)
	}
	return string(b)
}

func main() {
	lists := [][]string{}
	for l := 0; l < 20; l++ {
		seen := map[string]bool{}
		words := []string{}
		for len(words) < 400 {
			n := 8 + nextRandom()%9
			word := randomWord(n, 2)
			if !seen[word] {
				seen[word] = true
				words = append(words, word)
			}
		}
		lists = append(lists, words)
	}
	total, checksum := int64(0), int64(0)
	for r := 0; r < 50; r++ {
		for l := range lists {
			for _, a := range wordsAbbreviation(lists[l]) {
				total += int64(len(a))
				for i := 0; i < len(a); i++ {
					checksum = (checksum*31 + int64(a[i])) % 1000000007
				}
			}
		}
	}
	fmt.Printf("20 lists of 400 words, 50 rounds: %d letters, checksum %d\n", total, checksum)
}
