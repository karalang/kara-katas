// LeetCode #2328: Number of Increasing Paths in a Grid -- the bench, the
// ★ arm in Go. The cells sorted by value, largest first, and each cell's
// count of paths one plus its larger neighbours' counts, all of them
// already done. O(m n log(m n)).
package main

import (
	"fmt"
	"sort"
)

const mod = 1000000007

type cell struct{ value, r, c int64 }

func countPaths(grid [][]int64) int64 {
	m, n := int64(len(grid)), int64(len(grid[0]))
	cells := make([]cell, 0, m*n)
	for r := int64(0); r < m; r++ {
		for c := int64(0); c < n; c++ {
			cells = append(cells, cell{grid[r][c], r, c})
		}
	}
	sort.Slice(cells, func(i, j int) bool {
		a, b := cells[i], cells[j]
		if a.value != b.value {
			return a.value > b.value
		}
		if a.r != b.r {
			return a.r > b.r
		}
		return a.c > b.c
	})
	moves := [4][2]int64{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	from := make([][]int64, m)
	for r := range from {
		from[r] = make([]int64, n)
		for c := range from[r] {
			from[r][c] = 1
		}
	}
	var total int64
	for _, x := range cells {
		for _, d := range moves {
			nr, nc := x.r+d[0], x.c+d[1]
			if nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] > x.value {
				from[x.r][x.c] = (from[x.r][x.c] + from[nr][nc]) % mod
			}
		}
		total = (total + from[x.r][x.c]) % mod
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2328)
	grids := make([][][]int64, 10)
	for k := range grids {
		grids[k] = make([][]int64, 250)
		for r := range grids[k] {
			grids[k][r] = make([]int64, 400)
			for c := range grids[k][r] {
				grids[k][r][c] = nextRandom(&seed)%1000 + 1
			}
		}
	}
	var check int64
	for p := int64(0); p < 3; p++ {
		for k := 0; k < 10; k++ {
			check = (check*31 + countPaths(grids[k]) + p) % 1000000007
		}
	}
	fmt.Printf("3 passes over 10 grids of 10^5 cells: checksum %d\n", check)
}
