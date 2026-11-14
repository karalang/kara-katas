// LeetCode #1559: Detect Cycles in 2D Grid -- bench: the ★ arm (a search
// on a stack, each cell with the cell it came from) over 20 comb grids of
// 500 by 500 with no cycle, half with two cells made `a` to join two teeth
// in one, built once, each asked 5 times.
// Go mirror of cycles.kara.
package main

import "fmt"

type entry struct{ cell, from int64 }

func containsCycle(grid [][]rune) bool {
	rows := int64(len(grid))
	cols := int64(len(grid[0]))
	seen := make([]bool, rows*cols)
	dirs := [4][2]int64{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	for start := int64(0); start < rows*cols; start++ {
		if seen[start] {
			continue
		}
		seen[start] = true
		stack := []entry{{start, -1}}
		for len(stack) > 0 {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			r, c := top.cell/cols, top.cell%cols
			for _, d := range dirs {
				nr, nc := r+d[0], c+d[1]
				if nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] != grid[r][c] {
					continue
				}
				next := nr*cols + nc
				if next == top.from {
					continue
				}
				if seen[next] {
					return true
				}
				seen[next] = true
				stack = append(stack, entry{next, top.cell})
			}
		}
	}
	return false
}

var seed int64 = 1559

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func comb(size int64) [][]rune {
	alphabet := []rune("abcdefghijklmnopqrstuvwxyz")
	grid := make([][]rune, 0, size)
	for r := int64(0); r < size; r++ {
		row := make([]rune, 0, size)
		for c := int64(0); c < size; c++ {
			if r == 0 || c%2 == 0 {
				row = append(row, 'a')
			} else {
				row = append(row, alphabet[nextRandom()%25+1])
			}
		}
		grid = append(grid, row)
	}
	return grid
}

func main() {
	const size = 500
	grids := make([][][]rune, 0, 20)
	for g := 0; g < 20; g++ {
		grid := comb(size)
		if g%2 == 1 {
			r := nextRandom()%(size-2) + 1
			c := nextRandom()%(size/2-1)*2 + 1
			grid[r][c] = 'a'
			grid[r+1][c] = 'a'
		}
		grids = append(grids, grid)
	}
	var check, found int64
	for pass := int64(0); pass < 5; pass++ {
		for g, grid := range grids {
			cycle := containsCycle(grid)
			if cycle {
				found++
				check = mix(check, pass*20+int64(g))
			} else {
				check = mix(check, -1)
			}
		}
	}
	fmt.Printf("5 passes over 20 grids of 500 by 500: %d with a cycle, checksum %d\n", found, check)
}
