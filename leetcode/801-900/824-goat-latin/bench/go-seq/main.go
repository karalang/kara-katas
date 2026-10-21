// Benchmark for #824: Goat Latin -- the ★ arm (split, growing suffix).
//
// Mirrors goat_latin.kara: the sentence split at spaces, each word keeping
// a first vowel and moving a first consonant to the end, then "ma" and a
// run of 'a's kept in a buffer that grows by one letter per word.
package main

import (
	"fmt"
	"strings"
)

func isVowel(c byte) bool {
	return strings.IndexByte("aeiouAEIOU", c) >= 0
}

func toGoatLatin(sentence string) string {
	var answer []byte
	var tail []byte
	for _, word := range strings.Split(sentence, " ") {
		tail = append(tail, 'a')
		if len(answer) > 0 {
			answer = append(answer, ' ')
		}
		first := word[0]
		if isVowel(first) {
			answer = append(answer, word...)
		} else {
			answer = append(answer, word[1:]...)
			answer = append(answer, first)
		}
		answer = append(answer, "ma"...)
		answer = append(answer, tail...)
	}
	return string(answer)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 64
	rounds := 2000000
	letters := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	seed := int64(824)
	sentences := make([]string, 0, count)
	for g := 0; g < count; g++ {
		var s []byte
		for {
			length := 1 + nextRandom(&seed)%9
			extra := length
			if len(s) > 0 {
				extra++
			}
			if int64(len(s))+extra > 150 {
				break
			}
			if len(s) > 0 {
				s = append(s, ' ')
			}
			for i := int64(0); i < length; i++ {
				s = append(s, letters[nextRandom(&seed)%52])
			}
		}
		sentences = append(sentences, string(s))
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		answer := toGoatLatin(sentences[round%count])
		total += int64(len(answer))
		checksum = (checksum*131 + int64(answer[round%len(answer)])) % 1000000007
	}
	fmt.Printf("%d rounds of %d sentences: total %d, checksum %d\n", rounds, count, total, checksum)
}
