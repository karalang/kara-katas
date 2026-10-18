// LeetCode 750 — Number Of Corner Rectangles, bench: the ★ arm (pairs
// of rows) on a 200 x 200 grid that keeps changing.
// Mirrors count_corner_rectangles.kara.
package main

import "fmt"

func countCornerRectangles(grid [][]int64) int64 {
	m, n := len(grid), len(grid[0])
	var total int64
	for a := 0; a < m; a++ {
		for b := a + 1; b < m; b++ {
			var k int64
			for c := 0; c < n; c++ {
				if grid[a][c] == 1 && grid[b][c] == 1 {
					k++
				}
			}
			total += k * (k - 1) / 2
		}
	}
	return total
}

var seed int64 = 750

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds = 100
	grid := make([][]int64, 200)
	for r := range grid {
		grid[r] = make([]int64, 200)
		for c := range grid[r] {
			grid[r][c] = nextRandom() % 2
		}
	}
	var total, check int64
	for round := 0; round < rounds; round++ {
		for k := 0; k < 50; k++ {
			r := nextRandom() % 200
			c := nextRandom() % 200
			grid[r][c] = nextRandom() % 2
		}
		k := countCornerRectangles(grid)
		total += k
		check = (check*31 + k) % 1000000007
	}
	fmt.Printf("%d grids of 200 x 200: %d rectangles in all, checksum %d\n", rounds, total, check)
}
