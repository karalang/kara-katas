// LeetCode #1034: Coloring A Border -- bench
// Mirrors ../color_border.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

var dirs = [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}

func visit(grid [][]int64, r, c, color int64, seen [][]bool, out [][]int64) {
	seen[r][c] = true
	m := int64(len(grid))
	n := int64(len(grid[0]))
	border := false
	for _, d := range dirs {
		nr, nc := r+d[0], c+d[1]
		if nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr][nc] != grid[r][c] {
			border = true
		} else if !seen[nr][nc] {
			visit(grid, nr, nc, color, seen, out)
		}
	}
	if border {
		out[r][c] = color
	}
}

func colorBorder(grid [][]int64, row, col, color int64) [][]int64 {
	seen := make([][]bool, len(grid))
	out := make([][]int64, len(grid))
	for i := range grid {
		seen[i] = make([]bool, len(grid[0]))
		out[i] = append([]int64(nil), grid[i]...)
	}
	visit(grid, row, col, color, seen, out)
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count, starts, rounds := 100, 10, 20
	seed := int64(1034)
	grids := make([][][]int64, 0, count)
	type ask struct{ g, row, col, color int64 }
	asks := []ask{}
	for g := 0; g < count; g++ {
		grid := make([][]int64, 50)
		for i := range grid {
			grid[i] = make([]int64, 50)
			for j := range grid[i] {
				if nextRandom(&seed)%3 == 0 {
					grid[i][j] = 2
				} else {
					grid[i][j] = 1
				}
			}
		}
		grids = append(grids, grid)
		for s := 0; s < starts; s++ {
			row := nextRandom(&seed) % 50
			col := nextRandom(&seed) % 50
			color := nextRandom(&seed)%3 + 1
			asks = append(asks, ask{int64(g), row, col, color})
		}
	}
	var changed, check int64
	for round := 0; round < rounds; round++ {
		for _, a := range asks {
			grid := grids[a.g]
			painted := colorBorder(grid, a.row, a.col, a.color)
			for r := int64(0); r < 50; r++ {
				for c := int64(0); c < 50; c++ {
					if painted[r][c] != grid[r][c] {
						changed++
						check = (check*131 + r*50 + c) % 1000000007
					}
				}
			}
		}
	}
	fmt.Printf("%d grids of 50 by 50, %d starts each, %d rounds: %d squares changed, checksum %d\n", count, starts, rounds, changed, check)
}
