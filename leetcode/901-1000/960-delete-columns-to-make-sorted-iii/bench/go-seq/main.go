// Benchmark: LeetCode #960 Delete Columns to Make Sorted III -- the ★
// arm, longest chain, on 100 strings of 100 letters, LeetCode's largest.
// Mirrors min_deletion_size.kara, .c, .rs and .py.
package main

import (
	"fmt"
	"sort"
)

func minDeletionSize(strs []string) int {
	n := len(strs)
	m := len(strs[0])
	longest := make([]int, m)
	best := 0
	for j := 0; j < m; j++ {
		longest[j] = 1
		for k := 0; k < j; k++ {
			before := true
			for i := 0; i < n; i++ {
				if strs[i][k] > strs[i][j] {
					before = false
					break
				}
			}
			if before && longest[k]+1 > longest[j] {
				longest[j] = longest[k] + 1
			}
		}
		if longest[j] > best {
			best = longest[j]
		}
	}
	return m - best
}

var seed int64 = 960

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func nearlySorted(n, m int, letters int64, swaps int) []string {
	out := make([]string, n)
	for s := range out {
		b := make([]byte, m)
		for i := range b {
			b[i] = byte('a' + nextRandom()%letters)
		}
		sort.Slice(b, func(x, y int) bool { return b[x] < b[y] })
		for k := 0; k < swaps; k++ {
			p := nextRandom() % int64(m-1)
			b[p], b[p+1] = b[p+1], b[p]
		}
		out[s] = string(b)
	}
	return out
}

func main() {
	rounds := 40
	cases := make([][]string, 50)
	for i := range cases {
		cases[i] = nearlySorted(100, 100, int64(2+i%25), i%10)
	}
	total, check := 0, 0
	for r := 0; r < rounds; r++ {
		for i := 0; i < 50; i++ {
			d := minDeletionSize(cases[(r+i)%50])
			total += d
			check = (check*31 + d + i) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 50 cases of 100 strings of 100 letters: %d columns deleted, checksum %d\n", rounds, total, check)
}
