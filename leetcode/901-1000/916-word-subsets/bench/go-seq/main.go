// LeetCode #916: Word Subsets -- bench: Go mirror of every word of words2
// folded into one need in word_subsets.kara.
package main

import "fmt"

func counts(word string) [26]int64 {
	var count [26]int64
	for i := 0; i < len(word); i++ {
		count[word[i]-'a']++
	}
	return count
}

func wordSubsets(words1, words2 []string) []string {
	var need [26]int64
	for _, b := range words2 {
		count := counts(b)
		for c := 0; c < 26; c++ {
			if count[c] > need[c] {
				need[c] = count[c]
			}
		}
	}
	universal := []string{}
	for _, a := range words1 {
		count := counts(a)
		all := true
		for c := 0; c < 26; c++ {
			if count[c] < need[c] {
				all = false
			}
		}
		if all {
			universal = append(universal, a)
		}
	}
	return universal
}

var seed int64 = 916

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(length, letters int64) string {
	w := make([]byte, length)
	for i := range w {
		w[i] = byte(97 + nextRandom()%letters)
	}
	return string(w)
}

func main() {
	rounds := 200
	n := 50000
	words1 := make([]string, n)
	for i := range words1 {
		words1[i] = randomWord(10, 8)
	}
	total := 0
	var check int64
	for r := 0; r < rounds; r++ {
		words2 := []string{}
		for j := 0; j < 3; j++ {
			length := 1 + nextRandom()%3
			words2 = append(words2, randomWord(length, 8))
		}
		universal := wordSubsets(words1, words2)
		total += len(universal)
		for _, w := range universal {
			for i := 0; i < len(w); i++ {
				check = (check*31 + int64(w[i])) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d words: %d universal, checksum %d\n", rounds, n, total, check)
}
