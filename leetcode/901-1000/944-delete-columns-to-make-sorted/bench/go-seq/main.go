// Benchmark: LeetCode #944 Delete Columns to Make Sorted -- the ★ arm,
// column by column, on grids of 100 rows of 1000 letters, LeetCode's
// largest. Mirrors min_deletion_size.kara, .c, .rs and .py.
package main

import (
	"fmt"
	"sort"
)

func minDeletionSize(strs []string) int64 {
	n := len(strs)
	m := len(strs[0])
	var deleted int64
	for c := 0; c < m; c++ {
		r := 1
		for r < n && strs[r-1][c] <= strs[r][c] {
			r++
		}
		if r < n {
			deleted++
		}
	}
	return deleted
}

var seed int64 = 944

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count, n, m := 150, 20, 100, 1000
	grids := make([][]string, 0, count)
	for g := 0; g < count; g++ {
		columns := make([][]byte, m)
		for c := 0; c < m; c++ {
			column := make([]byte, n)
			for r := range column {
				column[r] = byte(nextRandom()%26 + 97)
			}
			sort.Slice(column, func(i, j int) bool { return column[i] < column[j] })
			if nextRandom()%2 == 0 {
				a := nextRandom() % int64(n)
				b := nextRandom() % int64(n)
				column[a], column[b] = column[b], column[a]
			}
			columns[c] = column
		}
		strs := make([]string, n)
		for r := 0; r < n; r++ {
			row := make([]byte, m)
			for c := 0; c < m; c++ {
				row[c] = columns[c][r]
			}
			strs[r] = string(row)
		}
		grids = append(grids, strs)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			d := minDeletionSize(grids[(r+i)%count])
			total += d
			check = (check*1000003 + d*int64(i+1)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d grids of %d rows of %d letters: %d deleted, checksum %d\n", rounds, count, n, m, total, check)
}
