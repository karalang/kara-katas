// LeetCode #720: Longest Word in Dictionary -- a trie, walked through
// word ends only. Benchmark mirror of the Kara trie arm: every word put
// in a trie with one array of 26 children per node, then a depth-first
// walk that steps only onto nodes where a word ends.
package main

import (
	"fmt"
	"strings"
)

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func deepest(next [][]int64, wordAt []int64, node int64, depth int64) (int64, int64) {
	bestDepth, bestWord := depth, wordAt[node]
	for c := 0; c < 26; c++ {
		child := next[node][c]
		if child != 0 && wordAt[child] >= 0 {
			d, w := deepest(next, wordAt, child, depth+1)
			if d > bestDepth {
				bestDepth, bestWord = d, w
			}
		}
	}
	return bestDepth, bestWord
}

func longestWord(words []string) string {
	next := [][]int64{make([]int64, 26)}
	wordAt := []int64{-1}
	for i, w := range words {
		node := int64(0)
		for j := 0; j < len(w); j++ {
			c := w[j] - 'a'
			if next[node][c] == 0 {
				next[node][c] = int64(len(next))
				next = append(next, make([]int64, 26))
				wordAt = append(wordAt, -1)
			}
			node = next[node][c]
		}
		wordAt[node] = int64(i)
	}
	_, w := deepest(next, wordAt, 0, 0)
	if w < 0 {
		return ""
	}
	return words[w]
}

func main() {
	seed := int64(720)
	var dicts [][]string
	for d := 0; d < 40; d++ {
		var words []string
		for k := 0; k < 1000; k++ {
			if len(words) > 0 && nextRandom(&seed)%4 != 0 {
				w := words[nextRandom(&seed)%int64(len(words))]
				if len(w) < 30 {
					w += string(rune(97 + nextRandom(&seed)%4))
				}
				words = append(words, w)
			} else {
				var b strings.Builder
				n := 1 + nextRandom(&seed)%3
				for j := int64(0); j < n; j++ {
					b.WriteByte(byte(97 + nextRandom(&seed)%4))
				}
				words = append(words, b.String())
			}
		}
		dicts = append(dicts, words)
	}
	sum := 0
	for round := int64(0); round < 300; round++ {
		for d := int64(0); d < 40; d++ {
			i := (round*7919 + d*104729) % 1000
			if len(dicts[d][i]) < 30 {
				dicts[d][i] += string(rune(97 + round%4))
			}
			sum += len(longestWord(dicts[d]))
		}
	}
	fmt.Printf("300 rounds of 40 dictionaries of 1000 words: sum %d\n", sum)
}
