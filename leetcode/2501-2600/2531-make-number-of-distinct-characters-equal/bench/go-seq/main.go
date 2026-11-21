// LeetCode #2531: Make Number of Distinct Characters Equal -- Go mirror of
// the benchmark (chars.kara): the same pairs, passes, order and checksum.
package main

import (
	"fmt"
	"strings"
)

func distinct(counts *[26]int64) int64 {
	var d int64
	for _, c := range counts {
		if c > 0 {
			d++
		}
	}
	return d
}

func isItPossible(word1, word2 string) bool {
	var one, two [26]int64
	for i := 0; i < len(word1); i++ {
		one[word1[i]-'a']++
	}
	for i := 0; i < len(word2); i++ {
		two[word2[i]-'a']++
	}
	for a := 0; a < 26; a++ {
		for b := 0; b < 26; b++ {
			if one[a] > 0 && two[b] > 0 {
				one[a]--
				one[b]++
				two[b]--
				two[a]++
				equal := distinct(&one) == distinct(&two)
				one[a]++
				one[b]--
				two[b]++
				two[a]--
				if equal {
					return true
				}
			}
		}
	}
	return false
}

var seed int64 = 2531

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(length, letters int64) string {
	var sb strings.Builder
	for i := int64(0); i < length; i++ {
		sb.WriteByte(byte('a' + nextRandom()%letters))
	}
	return sb.String()
}

func main() {
	words1 := make([]string, 1000)
	words2 := make([]string, 1000)
	for t := 0; t < 1000; t++ {
		l1 := nextRandom()%1000 + 1
		k1 := nextRandom()%26 + 1
		words1[t] = randomWord(l1, k1)
		l2 := nextRandom()%1000 + 1
		k2 := nextRandom()%26 + 1
		words2[t] = randomWord(l2, k2)
	}
	const passes = 24
	var check int64
	for p := int64(0); p < passes; p++ {
		start := check % 1000
		for i := int64(0); i < 1000; i++ {
			at := (start + i) % 1000
			var v int64 = 1
			if isItPossible(words1[at], words2[at]) {
				v = 2
			}
			check = (check*31 + v + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 1000 pairs of words: checksum %d\n", passes, check)
}
