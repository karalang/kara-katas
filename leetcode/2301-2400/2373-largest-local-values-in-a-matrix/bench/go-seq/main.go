// LeetCode #2373: Largest Local Values in a Matrix -- the bench, the ★ arm
// in Go: each cell of the answer is the largest of the nine values in the
// 3 x 3 block whose top left corner it names.
package main

import "fmt"

func largestLocal(grid [][]int64) [][]int64 {
	n := len(grid)
	out := [][]int64{}
	for i := 0; i < n-2; i++ {
		row := []int64{}
		for j := 0; j < n-2; j++ {
			most := int64(0)
			for di := 0; di < 3; di++ {
				for dj := 0; dj < 3; dj++ {
					most = max(most, grid[i+di][j+dj])
				}
			}
			row = append(row, most)
		}
		out = append(out, row)
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// grid a: 100 x 100 random values from 1 to 10 (a + 1)
	seed := int64(2373)
	grids := make([][][]int64, 0, 10)
	for a := int64(0); a < 10; a++ {
		grid := make([][]int64, 100)
		for i := range grid {
			grid[i] = make([]int64, 100)
			for j := range grid[i] {
				grid[i][j] = 1 + nextRandom(&seed)%(10*(a+1))
			}
		}
		grids = append(grids, grid)
	}
	check := int64(0)
	for p := int64(0); p < 200; p++ {
		for _, grid := range grids {
			for _, row := range largestLocal(grid) {
				for _, v := range row {
					check = (check*31 + v + p) % 1000000007
				}
			}
		}
	}
	fmt.Printf("200 passes over 10 grids of 100 x 100: checksum %d\n", check)
}
