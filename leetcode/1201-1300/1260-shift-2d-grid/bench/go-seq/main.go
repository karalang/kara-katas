// LeetCode #1260 bench, in Go: the ★ arm (each value at flat place p
// written to (p + k) % (m * n) of a new grid) on 200 random grids of 50 by
// 50 built once, each shifted by a random 0 to 100, 150 rounds; a corner and
// the middle of each result folded into a checksum.
package main

import "fmt"

func shiftGrid(grid [][]int64, k int64) [][]int64 {
	m := int64(len(grid))
	n := int64(len(grid[0]))
	total := m * n
	shifted := make([][]int64, m)
	for i := range shifted {
		shifted[i] = make([]int64, n)
	}
	for i := int64(0); i < m; i++ {
		for j := int64(0); j < n; j++ {
			to := (i*n + j + k) % total
			shifted[to/n][to%n] = grid[i][j]
		}
	}
	return shifted
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1260)
	var grids [][][]int64
	var shifts []int64
	for g := 0; g < 200; g++ {
		grid := make([][]int64, 50)
		for i := range grid {
			grid[i] = make([]int64, 50)
			for j := range grid[i] {
				grid[i][j] = nextRandom(&seed)%2001 - 1000
			}
		}
		grids = append(grids, grid)
		shifts = append(shifts, nextRandom(&seed)%101)
	}
	check := int64(0)
	for r := 0; r < 150; r++ {
		for g := 0; g < 200; g++ {
			s := shiftGrid(grids[g], shifts[g])
			check = (check*131 + s[0][0] + 1000) % 1000000007
			check = (check*131 + s[25][25] + 1000) % 1000000007
		}
	}
	fmt.Printf("150 rounds of 200 grids of 50 by 50: checksum %d\n", check)
}
