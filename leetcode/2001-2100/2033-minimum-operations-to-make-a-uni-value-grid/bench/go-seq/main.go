// LeetCode #2033: Minimum Operations to Make a Uni-Value Grid -- the ★ arm
// in Go, the same algorithm and workload as grid.kara: the values copied
// out of the grid and sorted per call.
package main

import (
	"fmt"
	"sort"
)

func minOperations(grid [][]int64, x int64) int64 {
	values := make([]int64, 0, len(grid)*len(grid[0]))
	for _, row := range grid {
		values = append(values, row...)
	}
	r := values[0] % x
	for _, v := range values {
		if v%x != r {
			return -1
		}
	}
	sort.Slice(values, func(i, j int) bool { return values[i] < values[j] })
	median := values[len(values)/2]
	var total int64
	for _, v := range values {
		d := v - median
		if d < 0 {
			d = -d
		}
		total += d / x
	}
	return total
}

var seed int64 = 2033

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grids := make([][][]int64, 20)
	for a := int64(0); a < 20; a++ {
		x := a%7 + 1
		base := nextRandom()%x + 1
		steps := (10000-base)/x + 1
		grid := make([][]int64, 200)
		for i := range grid {
			row := make([]int64, 250)
			for j := range row {
				hi := nextRandom()
				lo := nextRandom()
				row[j] = base + (hi*32768+lo)%steps*x
			}
			grid[i] = row
		}
		grids[a] = grid
	}
	var calls, sum, check int64
	for round := int64(0); round < 30; round++ {
		for a := int64(0); a < 20; a++ {
			x := a%7 + 1
			at := (round*997 + a*31) % 50000
			v := grids[a][at/250][at%250]
			if v+x <= 10000 {
				grids[a][at/250][at%250] = v + x
			} else {
				grids[a][at/250][at%250] = v - x
			}
			answer := minOperations(grids[a], x)
			calls++
			sum += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
