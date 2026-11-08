// LeetCode #1065: Index Pairs of a String -- the benchmark, the same
// every-start-against-every-word search as index_pairs.kara.
package main

import (
	"fmt"
	"sort"
	"strings"
)

type pair struct{ i, j int64 }

func indexPairs(text string, words []string) []pair {
	pairs := []pair{}
	for i := 0; i < len(text); i++ {
		for _, w := range words {
			if strings.HasPrefix(text[i:], w) {
				pairs = append(pairs, pair{int64(i), int64(i + len(w) - 1)})
			}
		}
	}
	sort.Slice(pairs, func(a, b int) bool {
		if pairs[a].i != pairs[b].i {
			return pairs[a].i < pairs[b].i
		}
		return pairs[a].j < pairs[b].j
	})
	return pairs
}

var seed int64 = 1065

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n, k int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom()%k)
	}
	return string(b)
}

// Up to `count` distinct words of 1 to `longest` letters over `k`: each
// drawn at random or, every other one, cut from the text.
func randomWords(text string, count, longest, k int64) []string {
	words := []string{}
	for w := int64(0); w < count; w++ {
		n := nextRandom()%longest + 1
		var word string
		if w%2 == 1 && n <= int64(len(text)) {
			at := nextRandom() % (int64(len(text)) - n + 1)
			word = text[at : at+n]
		} else {
			word = randomWord(n, k)
		}
		seen := false
		for _, v := range words {
			seen = seen || v == word
		}
		if !seen {
			words = append(words, word)
		}
	}
	return words
}

func main() {
	// 40 texts of 20000 letters over 2 to 4, each with up to 100 words of 1
	// to 12 letters, built once, then each answered
	texts := []string{}
	lists := [][]string{}
	for t := int64(0); t < 40; t++ {
		k := 2 + t%3
		text := randomWord(20000, k)
		lists = append(lists, randomWords(text, 100, 12, k))
		texts = append(texts, text)
	}
	var calls, count, check int64
	for t := 0; t < 40; t++ {
		pairs := indexPairs(texts[t], lists[t])
		count += int64(len(pairs))
		for _, p := range pairs {
			check = (check*31 + p.i*101 + p.j + 1) % 1000000007
		}
		calls++
	}
	fmt.Printf("%d calls: %d pairs, checksum %d\n", calls, count, check)
}
