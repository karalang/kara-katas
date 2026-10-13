// Benchmark for #472 -- Go mirror of the ★ arm (concatenated_words.kara):
// shortest first, each word broken against the words before it.
package main

import (
	"fmt"
	"sort"
)

func breaks(word string, known map[string]struct{}) bool {
	n := len(word)
	reach := make([]bool, n+1)
	reach[0] = true
	for end := 1; end <= n; end++ {
		for start := 0; start < end; start++ {
			if reach[start] {
				if _, ok := known[word[start:end]]; ok {
					reach[end] = true
					break
				}
			}
		}
	}
	return reach[n]
}

func findAllConcatenatedWordsInADict(words []string) []string {
	order := append([]string(nil), words...)
	sort.SliceStable(order, func(a, b int) bool { return len(order[a]) < len(order[b]) })
	known := make(map[string]struct{})
	var found []string
	for _, word := range order {
		if len(known) > 0 && breaks(word, known) {
			found = append(found, word)
		}
		known[word] = struct{}{}
	}
	return found
}

// ---- bench ------------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	size := 10000
	seed := int64(472)
	seen := make(map[string]struct{})
	var words []string
	for len(words) < size {
		w := ""
		if len(words) < 1000 {
			letters := 2 + nextRandom(&seed)%4
			for i := int64(0); i < letters; i++ {
				w += string(rune(97 + nextRandom(&seed)%4))
			}
		} else {
			parts := 2 + nextRandom(&seed)%2
			for i := int64(0); i < parts; i++ {
				w += words[nextRandom(&seed)%int64(len(words))]
			}
			if nextRandom(&seed)%4 == 0 {
				w += "e"
			}
		}
		if _, ok := seen[w]; len(w) <= 30 && !ok {
			seen[w] = struct{}{}
			words = append(words, w)
		}
	}
	rounds := 10
	found := 0
	hashSum := int64(0)
	for r := 0; r < rounds; r++ {
		got := findAllConcatenatedWordsInADict(words)
		found += len(got)
		for _, w := range got {
			h := int64(0)
			for i := 0; i < len(w); i++ {
				h = (h*31 + int64(w[i])) % 1000000007
			}
			hashSum = (hashSum + h) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d words: %d concatenated, hash sum %d\n", rounds, size, found, hashSum)
}
