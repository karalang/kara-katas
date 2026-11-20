// LeetCode #2352: Equal Row and Column Pairs -- the bench, the ★ arm in
// Go: the rows counted in a map keyed by the row, then each column built
// and looked up there. A slice cannot key a map, so the key is the row's
// values written into a string, 8 bytes each.
package main

import (
	"encoding/binary"
	"fmt"
)

func key(values []int64) string {
	b := make([]byte, 8*len(values))
	for i, v := range values {
		binary.LittleEndian.PutUint64(b[8*i:], uint64(v))
	}
	return string(b)
}

func equalPairs(grid [][]int64) int64 {
	n := len(grid)
	rows := make(map[string]int64)
	for _, row := range grid {
		rows[key(row)]++
	}
	total := int64(0)
	column := make([]int64, n)
	for j := 0; j < n; j++ {
		for i := 0; i < n; i++ {
			column[i] = grid[i][j]
		}
		total += rows[key(column)]
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// grid g is 200 x 200, cell (i, j) being (a i j + b) mod m, so that
	// rows repeat and match columns, with a in 1 to 5 and m in 2 to 10
	seed := int64(2352)
	grids := make([][][]int64, 0, 10)
	for g := 0; g < 10; g++ {
		a := 1 + nextRandom(&seed)%5
		b := nextRandom(&seed) % 10
		m := 2 + nextRandom(&seed)%9
		grid := make([][]int64, 200)
		for i := int64(0); i < 200; i++ {
			grid[i] = make([]int64, 200)
			for j := int64(0); j < 200; j++ {
				grid[i][j] = (a*i*j + b) % m
			}
		}
		grids = append(grids, grid)
	}
	check := int64(0)
	for p := int64(0); p < 40; p++ {
		for _, grid := range grids {
			check = (check*31 + equalPairs(grid) + p) % 1000000007
		}
	}
	fmt.Printf("40 passes over 10 grids of 200 x 200: checksum %d\n", check)
}
