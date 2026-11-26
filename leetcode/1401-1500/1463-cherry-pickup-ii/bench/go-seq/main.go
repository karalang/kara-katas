// LeetCode #1463 bench in Go: the ★ arm (the most cherries over each pair
// of robot columns, row by row) on the same 40 grids of 70 by 70.
package main

import "fmt"

func filled(cols int) [][]int32 {
	t := make([][]int32, cols)
	for i := range t {
		t[i] = make([]int32, cols)
		for j := range t[i] {
			t[i][j] = -1
		}
	}
	return t
}

func cherryPickup(grid [][]int32) int32 {
	rows, cols := len(grid), len(grid[0])
	best := filled(cols)
	best[0][cols-1] = grid[0][0] + grid[0][cols-1]
	for r := 1; r < rows; r++ {
		next := filled(cols)
		for a := 0; a < cols; a++ {
			for b := 0; b < cols; b++ {
				if best[a][b] < 0 {
					continue
				}
				for da := -1; da <= 1; da++ {
					for db := -1; db <= 1; db++ {
						x, y := a+da, b+db
						if x < 0 || x >= cols || y < 0 || y >= cols {
							continue
						}
						here := grid[r][x] + grid[r][y]
						if x == y {
							here = grid[r][x]
						}
						next[x][y] = max(next[x][y], best[a][b]+here)
					}
				}
			}
		}
		best = next
	}
	most := int32(-1)
	for _, row := range best {
		for _, v := range row {
			most = max(most, v)
		}
	}
	return most
}

var seed int64 = 1463

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grids := make([][][]int32, 40)
	for g := range grids {
		grids[g] = make([][]int32, 70)
		for r := range grids[g] {
			grids[g][r] = make([]int32, 70)
			for c := range grids[g][r] {
				grids[g][r][c] = int32(nextRandom() % 101)
			}
		}
	}
	var check int64
	for g := 0; g < 40; g++ {
		cell := check % 4900
		grids[g][cell/70][cell%70] = int32(check % 101)
		most := int64(cherryPickup(grids[g]))
		check = (check*31 + most) % 1000000007
	}
	fmt.Printf("40 grids of 70 by 70: checksum %d\n", check)
}
