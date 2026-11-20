// LeetCode #1268 bench, in Go: the ★ arm (the products sorted, a binary
// search for each prefix typed, and up to three products from there that
// start with it) on 100 random lists of 1000 words of 1 to 10 letters from
// `a` to `d` built once, each searched for its own 20-letter word, 100
// rounds; every suggestion folded into a checksum.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func suggestedProducts(products []string, searchWord string) [][]string {
	sorted := append([]string(nil), products...)
	sort.Strings(sorted)
	var out [][]string
	for end := 1; end <= len(searchWord); end++ {
		prefix := searchWord[:end]
		lo, hi := 0, len(sorted)
		for lo < hi {
			mid := (lo + hi) / 2
			if sorted[mid] < prefix {
				lo = mid + 1
			} else {
				hi = mid
			}
		}
		var list []string
		for i := lo; i < len(sorted) && len(list) < 3 && strings.HasPrefix(sorted[i], prefix); i++ {
			list = append(list, sorted[i])
		}
		out = append(out, list)
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomWord(longest int64, seed *int64) string {
	n := nextRandom(seed)%longest + 1
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom(seed)%4)
	}
	return string(b)
}

func main() {
	seed := int64(1268)
	lists := make([][]string, 100)
	searches := make([]string, 100)
	for l := range lists {
		lists[l] = make([]string, 1000)
		for i := range lists[l] {
			lists[l][i] = randomWord(10, &seed)
		}
		b := make([]byte, 20)
		for i := range b {
			b[i] = byte('a' + nextRandom(&seed)%4)
		}
		searches[l] = string(b)
	}
	var check int64
	for round := int64(0); round < 100; round++ {
		for l := range lists {
			for _, list := range suggestedProducts(lists[l], searches[l]) {
				check = (check*131 + int64(len(list)) + round) % 1000000007
				for _, w := range list {
					for i := 0; i < len(w); i++ {
						check = (check*131 + int64(w[i])) % 1000000007
					}
				}
			}
		}
	}
	fmt.Printf("100 rounds of 100 searches among 1000 words: checksum %d\n", check)
}
