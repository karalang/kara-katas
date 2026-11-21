// LeetCode #2500: Delete Greatest Value in Each Row -- Go mirror of the
// benchmark (greatest.kara): the same grids, passes and checksum; each ask
// copies the grid and sorts every row with slices.Sort.
package main

import (
	"fmt"
	"slices"
)

var seed int64 = 2500

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func deleteGreatestValue(grid [][]int64) int64 {
	rows := make([][]int64, len(grid))
	for r, row := range grid {
		rows[r] = slices.Clone(row)
		slices.Sort(rows[r])
	}
	var total int64
	for j := range rows[0] {
		var most int64
		for _, row := range rows {
			if row[j] > most {
				most = row[j]
			}
		}
		total += most
	}
	return total
}

func main() {
	const passes int64 = 32
	grids := make([][][]int64, 1000)
	for g := range grids {
		grid := make([][]int64, 50)
		for r := range grid {
			row := make([]int64, 50)
			for c := range row {
				row[c] = nextRandom()%100 + 1
			}
			grid[r] = row
		}
		grids[g] = grid
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for g := 0; g < 1000; g++ {
			r := check % 50
			c := check / 50 % 50
			was := grids[g][r][c]
			grids[g][r][c] = (check+p)%100 + 1
			check = (check*31 + deleteGreatestValue(grids[g]) + p) % 1000000007
			grids[g][r][c] = was
		}
	}
	fmt.Printf("%d passes over 1000 grids of 50 by 50: checksum %d\n", passes, check)
}
