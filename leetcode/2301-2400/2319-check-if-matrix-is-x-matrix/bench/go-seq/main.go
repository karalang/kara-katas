// LeetCode #2319: Check if Matrix Is X-Matrix -- the bench, the ★ arm in
// Go. One walk over the cells, a cell on either diagonal nonzero and any
// other zero, the first cell that breaks its rule ending the walk.
// O(n^2).
package main

import "fmt"

func checkXMatrix(grid [][]int64) bool {
	n := len(grid)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			on := i == j || i+j == n-1
			if on != (grid[i][j] != 0) {
				return false
			}
		}
	}
	return true
}

var seed int64 = 2319

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := 100
	grids := make([][][]int64, 0, 200)
	for g := 0; g < 200; g++ {
		grid := make([][]int64, 0, n)
		for i := 0; i < n; i++ {
			row := make([]int64, 0, n)
			for j := 0; j < n; j++ {
				value := nextRandom()%100000 + 1
				if i == j || i+j == n-1 {
					row = append(row, value)
				} else {
					row = append(row, 0)
				}
			}
			grid = append(grid, row)
		}
		grids = append(grids, grid)
	}
	var check int64
	for p := int64(0); p < 400; p++ {
		for g := 0; g < 200; g++ {
			punch := nextRandom()%2 == 0
			i := nextRandom() % int64(n)
			j := nextRandom() % int64(n)
			old := grids[g][i][j]
			if punch {
				if old == 0 {
					grids[g][i][j] = p + 1
				} else {
					grids[g][i][j] = 0
				}
			}
			isX := checkXMatrix(grids[g])
			grids[g][i][j] = old
			v := int64(1)
			if isX {
				v = 2
			}
			check = (check*31 + v + p) % 1000000007
		}
	}
	fmt.Printf("400 passes over 200 grids of 100 by 100: checksum %d\n", check)
}
