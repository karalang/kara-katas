// LeetCode 792 — Number of Matching Subsequences: the bench, in Go.
// Mirrors num_matching_subseq.kara: every word waits in the bucket of
// the next letter it needs, and s is walked once; a bucket is taken
// whole, left empty, and walked.
package main

import "fmt"

type wait struct {
	w, matched int
}

func numMatchingSubseq(s string, words []string) int64 {
	var waiting [26][]wait
	for i, word := range words {
		waiting[word[0]-'a'] = append(waiting[word[0]-'a'], wait{i, 0})
	}
	var count int64
	for i := 0; i < len(s); i++ {
		c := s[i] - 'a'
		moving := waiting[c]
		waiting[c] = nil
		for _, m := range moving {
			word := words[m.w]
			if m.matched+1 == len(word) {
				count++
			} else {
				next := word[m.matched+1] - 'a'
				waiting[next] = append(waiting[next], wait{m.w, m.matched + 1})
			}
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomWord(seed *int64, length, letters int64) string {
	word := make([]byte, length)
	for i := range word {
		word[i] = byte(97 + nextRandom(seed)%letters)
	}
	return string(word)
}

func main() {
	seed := int64(792)
	strings := make([]string, 0, 16)
	for k := 0; k < 16; k++ {
		letters := 13 + nextRandom(&seed)%14
		strings = append(strings, randomWord(&seed, 50000, letters))
	}
	lists := make([][]string, 0, 64)
	for k := 0; k < 64; k++ {
		words := make([]string, 0, 5000)
		for i := 0; i < 5000; i++ {
			length := 1 + nextRandom(&seed)%50
			words = append(words, randomWord(&seed, length, 26))
		}
		lists = append(lists, words)
	}
	rounds := 4000
	var total, check int64
	for r := 0; r < rounds; r++ {
		count := numMatchingSubseq(strings[r%16], lists[(r/16)%64])
		total += count
		check = (check*131 + count + 1) % 1000000007
	}
	fmt.Printf("%d rounds of 5000 words: %d matching, checksum %d\n", rounds, total, check)
}
