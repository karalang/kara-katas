// LeetCode #1030: Matrix Cells in Distance Order -- bench
// Mirrors ../cells_order.kara; see ../../README.md § Benchmarks.

package main

import (
	"fmt"
	"sort"
)

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func allCellsDistOrder(rows, cols, rCenter, cCenter int64) [][]int64 {
	cells := [][]int64{}
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			cells = append(cells, []int64{r, c})
		}
	}
	sort.SliceStable(cells, func(i, j int) bool {
		return abs(cells[i][0]-rCenter)+abs(cells[i][1]-cCenter) < abs(cells[j][0]-rCenter)+abs(cells[j][1]-cCenter)
	})
	return cells
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 300
	seed := int64(1030)
	centres := [][2]int64{}
	for k := 0; k < count; k++ {
		r0 := nextRandom(&seed) % 100
		c0 := nextRandom(&seed) % 100
		centres = append(centres, [2]int64{r0, c0})
	}
	var total, check int64
	for _, rc := range centres {
		r0, c0 := rc[0], rc[1]
		cells := allCellsDistOrder(100, 100, r0, c0)
		var weighted int64
		for i := range cells {
			weighted += int64(i+1) * (abs(cells[i][0]-r0) + abs(cells[i][1]-c0))
		}
		total += weighted
		check = (check*131 + weighted) % 1000000007
	}
	fmt.Printf("%d centres on a 100x100 grid: sum %d, checksum %d\n", count, total, check)
}
