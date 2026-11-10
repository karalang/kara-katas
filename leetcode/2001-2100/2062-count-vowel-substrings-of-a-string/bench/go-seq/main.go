// LeetCode #2062: Count Vowel Substrings of a String -- Go mirror of the ★
// arm's benchmark (vowels.kara): 20000 words of 100 letters, each a vowel
// with chance 90 in 100, else one of `xyz`; the vowels met from each start
// in a `map[rune]bool`.
package main

import (
	"fmt"
	"strings"
)

func isVowel(c rune) bool { return strings.ContainsRune("aeiou", c) }

func countVowelSubstrings(word string) int64 {
	letters := []rune(word)
	count := int64(0)
	for i := range letters {
		met := map[rune]bool{}
		for j := i; j < len(letters); j++ {
			if !isVowel(letters[j]) {
				break
			}
			met[letters[j]] = true
			if len(met) == 5 {
				count++
			}
		}
	}
	return count
}

var seed int64 = 2062

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wordOf(n, p int64) string {
	vowels := []rune("aeiou")
	others := []rune("xyz")
	out := []rune{}
	for k := int64(0); k < n; k++ {
		if nextRandom()%100 < p {
			out = append(out, vowels[nextRandom()%5])
		} else {
			out = append(out, others[nextRandom()%3])
		}
	}
	return string(out)
}

func main() {
	total, check := int64(0), int64(0)
	for t := 0; t < 20000; t++ {
		a := countVowelSubstrings(wordOf(100, 90))
		total += a
		check = (check*31 + a) % 1000000007
	}
	fmt.Printf("20000 words: sum %d, checksum %d\n", total, check)
}
