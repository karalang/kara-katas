// Benchmark for #840: Magic Squares In Grid -- the ★ arm (the centre first).
//
// Mirrors magic_squares_in_grid.kara: each 3 by 3 window is looked at
// only if its centre is 5; then its nine numbers must be 1 to 9, each
// once, kept as bits of a mask, its rows and columns must add up to 15,
// and each diagonal's two corners to 10.
package main

import "fmt"

func isMagic(grid [][]int64, r, c int) bool {
	if grid[r+1][c+1] != 5 {
		return false
	}
	mask := int64(0)
	for i := r; i < r+3; i++ {
		for j := c; j < c+3; j++ {
			v := grid[i][j]
			if v < 1 || v > 9 {
				return false
			}
			mask |= 1 << v
		}
	}
	if mask != 1022 {
		return false
	}
	for k := 0; k < 3; k++ {
		if grid[r+k][c]+grid[r+k][c+1]+grid[r+k][c+2] != 15 {
			return false
		}
		if grid[r][c+k]+grid[r+1][c+k]+grid[r+2][c+k] != 15 {
			return false
		}
	}
	return grid[r][c]+grid[r+2][c+2] == 10 && grid[r][c+2]+grid[r+2][c] == 10
}

func numMagicSquaresInside(grid [][]int64) int64 {
	rows, cols := len(grid), len(grid[0])
	count := int64(0)
	for r := 0; r < rows-2; r++ {
		for c := 0; c < cols-2; c++ {
			if isMagic(grid, r, c) {
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
	// 64 grids drawn once, each LeetCode's largest, 10 by 10, of numbers
	// 0 to 15 with 12 squares of 3 by 3 stamped on it: the Lo Shu turned
	// or mirrored, a square of 5s, or the Lo Shu with 1 added to every
	// number. Each round changes one cell of the next grid and counts its
	// magic squares.
	const count, rounds = 64, 14000000
	loShu := [3][3]int64{{4, 9, 2}, {3, 5, 7}, {8, 1, 6}}
	seed := int64(840)
	grids := make([][][]int64, 0, count)
	for g := 0; g < count; g++ {
		grid := make([][]int64, 10)
		for i := range grid {
			grid[i] = make([]int64, 10)
			for j := range grid[i] {
				grid[i][j] = nextRandom(&seed) % 16
			}
		}
		for p := 0; p < 12; p++ {
			turn := nextRandom(&seed) % 8
			kind := nextRandom(&seed) % 3
			r := int(nextRandom(&seed) % 8)
			c := int(nextRandom(&seed) % 8)
			for i := 0; i < 3; i++ {
				for j := 0; j < 3; j++ {
					a, b := i, j
					if turn >= 4 {
						b = 2 - j
					}
					for t := int64(0); t < turn%4; t++ {
						a, b = 2-b, a
					}
					if kind == 1 {
						grid[r+i][c+j] = 5
					} else {
						grid[r+i][c+j] = loShu[a][b] + kind/2
					}
				}
			}
		}
		grids = append(grids, grid)
	}
	total, checksum := int64(0), int64(0)
	for round := int64(0); round < rounds; round++ {
		g := round % count
		cell := round * 7 % 100
		grids[g][cell/10][cell%10] = round % 16
		magic := numMagicSquaresInside(grids[g])
		total += magic
		checksum = (checksum*31 + magic + round) % 1000000007
	}
	fmt.Printf("%d rounds of %d grids: %d magic squares, checksum %d\n", rounds, count, total, checksum)
}
