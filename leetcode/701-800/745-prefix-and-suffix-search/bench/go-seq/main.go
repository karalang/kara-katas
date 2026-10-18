// LeetCode 745 — Prefix and Suffix Search, bench: the ★ arm (every
// prefix-suffix pair of every word in a map) on filters of 10000
// words, each asked 10000 queries. Mirrors prefix_and_suffix_search.kara.
package main

import (
	"fmt"
	"strings"
)

type WordFilter struct {
	keys map[string]int64
}

func newWordFilter(words []string) WordFilter {
	keys := make(map[string]int64)
	for i, w := range words {
		n := len(w)
		for p := 0; p <= n; p++ {
			for s := 0; s <= n; s++ {
				var key strings.Builder
				key.WriteString(w[:p])
				key.WriteByte('{')
				key.WriteString(w[s:])
				keys[key.String()] = int64(i)
			}
		}
	}
	return WordFilter{keys}
}

func (t WordFilter) f(pref, suff string) int64 {
	if i, ok := t.keys[pref+"{"+suff]; ok {
		return i
	}
	return -1
}

var seed int64 = 745

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(longest, letters int64) string {
	n := 1 + nextRandom()%longest
	b := make([]byte, 0, n)
	for i := int64(0); i < n; i++ {
		b = append(b, byte(97+nextRandom()%letters))
	}
	return string(b)
}

func main() {
	rounds := 5
	var found, total int64
	for r := 0; r < rounds; r++ {
		words := make([]string, 0)
		for i := 0; i < 10000; i++ {
			words = append(words, randomWord(7, 5))
		}
		filter := newWordFilter(words)
		for q := 0; q < 10000; q++ {
			pref := randomWord(4, 5)
			suff := randomWord(4, 5)
			got := filter.f(pref, suff)
			if got != -1 {
				found++
				total += got
			}
		}
	}
	fmt.Printf("%d rounds of 10000 words and 10000 queries: %d found, indices sum to %d\n", rounds, found, total)
}
