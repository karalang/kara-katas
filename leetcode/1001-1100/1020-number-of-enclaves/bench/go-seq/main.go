// LeetCode #1020: Number of Enclaves -- bench
// Mirrors ../enclaves.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

type cell struct{ i, j int64 }

func numEnclaves(grid [][]int64) int64 {
	m := int64(len(grid))
	n := int64(len(grid[0]))
	land := make([][]int64, m)
	for i := range grid {
		land[i] = append([]int64(nil), grid[i]...)
	}
	stack := []cell{}
	for i := int64(0); i < m; i++ {
		for j := int64(0); j < n; j++ {
			if (i == 0 || j == 0 || i == m-1 || j == n-1) && land[i][j] == 1 {
				land[i][j] = 0
				stack = append(stack, cell{i, j})
			}
		}
	}
	steps := [4][2]int64{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	for len(stack) > 0 {
		c := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		for _, s := range steps {
			a, b := c.i+s[0], c.j+s[1]
			if a >= 0 && a < m && b >= 0 && b < n && land[a][b] == 1 {
				land[a][b] = 0
				stack = append(stack, cell{a, b})
			}
		}
	}
	var left int64
	for _, row := range land {
		for _, c := range row {
			left += c
		}
	}
	return left
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 100, 20
	seed := int64(1020)
	grids := [][][]int64{}
	var cells int64
	for g := 0; g < count; g++ {
		m := nextRandom(&seed)%500 + 1
		n := nextRandom(&seed)%500 + 1
		land := 2 + nextRandom(&seed)%5
		grid := [][]int64{}
		for i := int64(0); i < m; i++ {
			row := []int64{}
			for j := int64(0); j < n; j++ {
				if nextRandom(&seed)%8 < land {
					row = append(row, 1)
				} else {
					row = append(row, 0)
				}
			}
			grid = append(grid, row)
		}
		cells += m * n
		grids = append(grids, grid)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, grid := range grids {
			a := numEnclaves(grid)
			total += a
			check = (check*31 + a) % 1000000007
		}
	}
	fmt.Printf("%d grids, %d cells, %d rounds: %d enclaves, checksum %d\n", count, cells, rounds, total, check)
}
