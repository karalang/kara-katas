// LeetCode #955: Delete Columns to Make Sorted II -- Go mirror of the Kara
// bench program (pairs settled).
package main

import (
	"fmt"
	"sort"
)

func minDeletionSize(strs []string) int64 {
	n := len(strs)
	m := len(strs[0])
	settled := make([]bool, n)
	deleted := int64(0)
	for c := 0; c < m; c++ {
		breaks := false
		for i := 0; i < n-1; i++ {
			if !settled[i] && strs[i][c] > strs[i+1][c] {
				breaks = true
				break
			}
		}
		if breaks {
			deleted++
			continue
		}
		for i := 0; i < n-1; i++ {
			if strs[i][c] < strs[i+1][c] {
				settled[i] = true
			}
		}
	}
	return deleted
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	rounds, count, n, m := 120, 200, 100, 100
	seed := int64(955)
	sets := [][]string{}
	for s := 0; s < count; s++ {
		letters := int64(2 + s%3)
		strs := make([]string, 0, n)
		for i := 0; i < n; i++ {
			w := make([]byte, m)
			for c := 0; c < m; c++ {
				w[c] = byte('a' + nextRandom(&seed)%letters)
			}
			strs = append(strs, string(w))
		}
		p := s % 12
		sort.SliceStable(strs, func(i, j int) bool { return strs[i][:p] < strs[j][:p] })
		sets = append(sets, strs)
	}
	total, check := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			k := (r + i) % count
			d := minDeletionSize(sets[k])
			total += d
			check = (check*31 + d) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d sets of %d strings of %d letters: %d columns deleted, checksum %d\n", rounds, count, n, m, total, check)
}
