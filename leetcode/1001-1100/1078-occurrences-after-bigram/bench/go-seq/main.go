// LeetCode #1078 bench, Go mirror of occurrences.kara: the same texts,
// bigrams, rounds and checksum.
package main

import (
	"fmt"
	"strings"
)

func findOccurrences(text, first, second string) []string {
	words := strings.Split(text, " ")
	var out []string
	for i := 2; i < len(words); i++ {
		if words[i-2] == first && words[i-1] == second {
			out = append(out, words[i])
		}
	}
	return out
}

var seed int64 = 1078

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(longest, k int64) string {
	n := nextRandom()%longest + 1
	b := make([]byte, 0, n)
	for i := int64(0); i < n; i++ {
		b = append(b, byte('a'+nextRandom()%k))
	}
	return string(b)
}

func main() {
	const rounds = 300
	vocabulary := make([]string, 12)
	for i := range vocabulary {
		vocabulary[i] = randomWord(4, 3)
	}
	var texts, firsts, seconds []string
	var owner []int
	for t := 0; t < 100; t++ {
		var words []string
		length := int64(-1)
		for {
			w := vocabulary[nextRandom()%12]
			if length+1+int64(len(w)) > 1000 {
				break
			}
			length += 1 + int64(len(w))
			words = append(words, w)
		}
		for q := 0; q < 8; q++ {
			if nextRandom()%4 < 3 {
				at := nextRandom() % int64(len(words)-1)
				firsts = append(firsts, words[at])
				seconds = append(seconds, words[at+1])
			} else {
				firsts = append(firsts, vocabulary[nextRandom()%12])
				seconds = append(seconds, vocabulary[nextRandom()%12])
			}
			owner = append(owner, t)
		}
		texts = append(texts, strings.Join(words, " "))
	}
	queries := len(firsts)
	var found, check int64
	for r := 0; r < rounds; r++ {
		for j := 0; j < queries; j++ {
			q := (j*7 + r) % queries
			out := findOccurrences(texts[owner[q]], firsts[q], seconds[q])
			found += int64(len(out))
			for _, w := range out {
				for i := 0; i < len(w); i++ {
					check = (check*31 + int64(w[i])) % 1000000007
				}
			}
			check = (check*31 + int64(len(out))) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d bigrams over 100 texts: %d words found, checksum %d\n", rounds, queries, found, check)
}
