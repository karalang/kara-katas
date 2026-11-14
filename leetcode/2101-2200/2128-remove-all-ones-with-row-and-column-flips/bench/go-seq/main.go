// LeetCode #2128: Remove All Ones With Row and Column Flips -- the
// benchmark, the same algorithm as flips.kara.
package main

import "fmt"

func removeOnes(grid [][]int64) bool {
	first := grid[0]
	for _, row := range grid {
		for j := range row {
			if row[j]^row[0] != first[j]^first[0] {
				return false
			}
		}
	}
	return true
}

var seed int64 = 2128

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 300
	grids := make([][][]int64, 20)
	for k := range grids {
		columns := make([]int64, n)
		for j := range columns {
			columns[j] = nextRandom() % 2
		}
		grids[k] = make([][]int64, n)
		for i := range grids[k] {
			r := nextRandom() % 2
			row := make([]int64, n)
			for j, c := range columns {
				row[j] = c ^ r
			}
			grids[k][i] = row
		}
	}
	var cleared, check int64
	for round := int64(0); round < 100; round++ {
		for k := int64(0); k < 20; k++ {
			r := nextRandom() % n
			for j := range grids[k][r] {
				grids[k][r][j] = 1 - grids[k][r][j]
			}
			broken := nextRandom()%2 == 0
			i := nextRandom() % n
			j := nextRandom() % n
			if broken {
				grids[k][i][j] = 1 - grids[k][i][j]
			}
			if removeOnes(grids[k]) {
				cleared++
				check = (check*31 + round*20 + k) % 1000000007
			}
			if broken {
				grids[k][i][j] = 1 - grids[k][i][j]
			}
		}
	}
	fmt.Printf("2000 solves: %d cleared, checksum %d\n", cleared, check)
}
