// LeetCode #1233 bench: the ★ arm in Go, over the same 10 lists of
// 4 · 10^4 folders and 10 passes as the Kāra bench.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func removeSubfolders(folder []string) []string {
	sorted := append([]string(nil), folder...)
	sort.Strings(sorted)
	kept := []string{}
	for _, f := range sorted {
		if len(kept) == 0 || !strings.HasPrefix(f, kept[len(kept)-1]+"/") {
			kept = append(kept, f)
		}
	}
	return kept
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	letters := []string{"a", "b", "c", "d", "e", "f", "g", "h"}
	seed := int64(1233)
	lists := [][]string{}
	for l := 0; l < 10; l++ {
		seen := map[string]bool{}
		many := []string{}
		for len(many) < 40000 {
			d := nextRandom(&seed)%4 + 1
			f := ""
			for level := int64(0); level < d; level++ {
				f += "/"
				k := 2
				if level == 0 {
					k = 4
				}
				for i := 0; i < k; i++ {
					f += letters[nextRandom(&seed)%8]
				}
			}
			if !seen[f] {
				seen[f] = true
				many = append(many, f)
			}
		}
		lists = append(lists, many)
	}
	kept := 0
	for pass := 0; pass < 10; pass++ {
		for _, list := range lists {
			kept += len(removeSubfolders(list))
		}
	}
	fmt.Printf("10 lists of 40000 folders, 10 passes: %d kept\n", kept)
}
