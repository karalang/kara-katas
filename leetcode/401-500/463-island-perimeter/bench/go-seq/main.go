// Benchmark for #463: mirror of island_perimeter.kara (the ★ arm: four
// sides per land cell, less two per shared edge) on the same workload.
package main

import (
	"fmt"
	"slices"
)

func islandPerimeter(grid [][]int64) int64 {
	land := int64(0)
	shared := int64(0)
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid[i]); j++ {
			if grid[i][j] == 1 {
				land++
				if j+1 < len(grid[i]) && grid[i][j+1] == 1 {
					shared++
				}
				if i+1 < len(grid) && grid[i+1][j] == 1 {
					shared++
				}
			}
		}
	}
	return 4*land - 2*shared
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

// A random walk of land on a rows x cols sea, then every lake filled in.
func randomIsland(rows, cols, steps int64, seed *int64) [][]int64 {
	grid := make([][]int64, rows)
	sea := make([][]bool, rows)
	for r := range grid {
		grid[r] = make([]int64, cols)
		sea[r] = make([]bool, cols)
	}
	i := nextRandom(seed) % rows
	j := nextRandom(seed) % cols
	grid[i][j] = 1
	for s := int64(0); s < steps; s++ {
		d := nextRandom(seed) % 4
		if d == 0 && i > 0 {
			i--
		} else if d == 1 && i+1 < rows {
			i++
		} else if d == 2 && j > 0 {
			j--
		} else if d == 3 && j+1 < cols {
			j++
		}
		grid[i][j] = 1
	}
	queue := [][2]int64{}
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			if (r == 0 || c == 0 || r == rows-1 || c == cols-1) && grid[r][c] == 0 {
				sea[r][c] = true
				queue = append(queue, [2]int64{r, c})
			}
		}
	}
	steps4 := [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head][0], queue[head][1]
		for _, d := range steps4 {
			nr, nc := r+d[0], c+d[1]
			if nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 0 && !sea[nr][nc] {
				sea[nr][nc] = true
				queue = append(queue, [2]int64{nr, nc})
			}
		}
	}
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			if !sea[r][c] {
				grid[r][c] = 1
			}
		}
	}
	return grid
}

func main() {
	const size int64 = 1000
	const islands = 2
	const rounds = 200
	seed := int64(463)
	grids := [][][]int64{}
	tops := []int64{}
	shores := [][]int64{}
	for g := 0; g < islands; g++ {
		inner := randomIsland(size-2, size-2, (size-2)*(size-2), &seed)
		grid := [][]int64{make([]int64, size)}
		for _, row := range inner {
			wide := []int64{0}
			wide = append(wide, row...)
			wide = append(wide, 0)
			grid = append(grid, wide)
		}
		grid = append(grid, make([]int64, size))
		top := int64(0)
		for !slices.Contains(grid[top], 1) {
			top++
		}
		shore := []int64{}
		for j := int64(0); j < size; j++ {
			if grid[top][j] == 1 {
				shore = append(shore, j)
			}
		}
		grids = append(grids, grid)
		tops = append(tops, top)
		shores = append(shores, shore)
	}
	total := int64(0)
	checksum := int64(0)
	for r := 0; r < rounds; r++ {
		for g := 0; g < islands; g++ {
			j := shores[g][nextRandom(&seed)%int64(len(shores[g]))]
			above := tops[g] - 1
			grids[g][above][j] = 1
			perimeter := islandPerimeter(grids[g])
			grids[g][above][j] = 0
			total += perimeter
			checksum = (checksum*31 + perimeter) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d islands of %dx%d: perimeter %d in all, checksum %d\n", rounds, islands, size, size, total, checksum)
}
