// LeetCode #2304: Minimum Path Cost in a Grid -- the bench, the ★ arm in
// Go. Row by row, each column of the next row takes the least over the
// row before of the cost so far plus the move, plus its own value.
package main

import (
	"fmt"
	"math"
)

func minPathCost(grid [][]int64, moveCost [][]int64) int64 {
	n := len(grid[0])
	best := append([]int64(nil), grid[0]...)
	for r := 1; r < len(grid); r++ {
		next := make([]int64, n)
		for j := 0; j < n; j++ {
			least := int64(math.MaxInt64)
			for k := 0; k < n; k++ {
				if c := best[k] + moveCost[grid[r-1][k]][j]; c < least {
					least = c
				}
			}
			next[j] = least + grid[r][j]
		}
		best = next
	}
	least := best[0]
	for _, b := range best[1:] {
		if b < least {
			least = b
		}
	}
	return least
}

var seed int64 = 2304

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grids := make([][][]int64, 20)
	tables := make([][][]int64, 20)
	for a := 0; a < 20; a++ {
		values := make([]int64, 2500)
		for i := range values {
			values[i] = int64(i)
		}
		for i := int64(2499); i >= 1; i-- {
			j := nextRandom() % (i + 1)
			values[i], values[j] = values[j], values[i]
		}
		grid := make([][]int64, 50)
		for r := 0; r < 50; r++ {
			grid[r] = values[r*50 : (r+1)*50]
		}
		grids[a] = grid
		table := make([][]int64, 2500)
		for v := range table {
			row := make([]int64, 50)
			for j := range row {
				row[j] = nextRandom()%100 + 1
			}
			table[v] = row
		}
		tables[a] = table
	}
	var check int64
	for p := 0; p < 40; p++ {
		for a := 0; a < 20; a++ {
			check = (check*31 + minPathCost(grids[a], tables[(a+p)%20])) % 1000000007
		}
	}
	fmt.Printf("40 passes over 20 grids of 50 by 50: checksum %d\n", check)
}
