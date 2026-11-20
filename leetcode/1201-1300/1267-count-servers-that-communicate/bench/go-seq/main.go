// LeetCode #1267 bench, in Go: the ★ arm (the servers in each row and each
// column counted, then each server that shares its row or column with
// another counted) on 100 random 100-by-100 grids built once, a cell a
// server one time in 2 to 9, 300 rounds; every answer folded into a
// checksum.
package main

import "fmt"

func countServers(grid [][]int64) int64 {
	m, n := len(grid), len(grid[0])
	rows := make([]int64, m)
	cols := make([]int64, n)
	for r := 0; r < m; r++ {
		for c := 0; c < n; c++ {
			if grid[r][c] == 1 {
				rows[r]++
				cols[c]++
			}
		}
	}
	var count int64
	for r := 0; r < m; r++ {
		for c := 0; c < n; c++ {
			if grid[r][c] == 1 && (rows[r] > 1 || cols[c] > 1) {
				count++
			}
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1267)
	grids := make([][][]int64, 100)
	for g := range grids {
		odds := nextRandom(&seed)%8 + 2
		grids[g] = make([][]int64, 100)
		for r := range grids[g] {
			grids[g][r] = make([]int64, 100)
			for c := range grids[g][r] {
				if nextRandom(&seed)%odds == 0 {
					grids[g][r][c] = 1
				}
			}
		}
	}
	var check int64
	for round := int64(0); round < 300; round++ {
		for _, g := range grids {
			check = (check*131 + countServers(g) + round) % 1000000007
		}
	}
	fmt.Printf("300 rounds of 100 grids of 100 by 100: checksum %d\n", check)
}
