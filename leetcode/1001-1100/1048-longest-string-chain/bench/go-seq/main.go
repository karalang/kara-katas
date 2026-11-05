// LeetCode #1048: Longest String Chain -- Go mirror of
// bench/longest_chain.kara: the words sorted by length, and a map from
// word to the longest chain ending there.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 1048

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func longestStrChain(words []string) int64 {
	sorted := append([]string(nil), words...)
	sort.SliceStable(sorted, func(a, b int) bool { return len(sorted[a]) < len(sorted[b]) })
	chain := map[string]int64{}
	var best int64
	for _, w := range sorted {
		var here int64 = 1
		for i := 0; i < len(w); i++ {
			pred := w[:i] + w[i+1:]
			if n, ok := chain[pred]; ok && n+1 > here {
				here = n + 1
			}
		}
		chain[w] = here
		if here > best {
			best = here
		}
	}
	return best
}

func main() {
	lists, count, rounds := 100, 2000, 5
	all := make([][]string, 0, lists)
	for l := 0; l < lists; l++ {
		words := make([]string, 0, count)
		for k := 0; k < count; k++ {
			n := nextRandom()%16 + 1
			b := make([]byte, n)
			for i := range b {
				b[i] = byte('a' + nextRandom()%3)
			}
			words = append(words, string(b))
		}
		all = append(all, words)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, words := range all {
			answer := longestStrChain(words)
			total += answer
			check = (check*131 + answer) % 1000000007
		}
	}
	fmt.Printf("%d lists of %d words, %d rounds: total %d, checksum %d\n", lists, count, rounds, total, check)
}
