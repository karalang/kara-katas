// LeetCode #1591: Strange Printer II -- the bench in Go, mirroring
// printer.kara: bounding rectangles, an order matrix, Kahn's algorithm.
package main

import "fmt"

func isPrintable(grid [][]int32) bool {
	rows, cols := int64(len(grid)), int64(len(grid[0]))
	var top, bottom, left, right, before [61]int64
	for k := 0; k < 61; k++ {
		top[k], bottom[k], left[k], right[k] = rows, -1, cols, -1
	}
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			k := grid[r][c]
			top[k] = min(top[k], r)
			bottom[k] = max(bottom[k], r)
			left[k] = min(left[k], c)
			right[k] = max(right[k], c)
		}
	}
	after := make([][]bool, 61)
	for k := range after {
		after[k] = make([]bool, 61)
	}
	for k := 1; k < 61; k++ {
		for r := top[k]; r < bottom[k]+1; r++ {
			for c := left[k]; c < right[k]+1; c++ {
				other := grid[r][c]
				if int(other) != k && !after[k][other] {
					after[k][other] = true
					before[other]++
				}
			}
		}
	}
	ready := []int{}
	for k := 1; k < 61; k++ {
		if before[k] == 0 {
			ready = append(ready, k)
		}
	}
	taken := 0
	for len(ready) > 0 {
		k := ready[len(ready)-1]
		ready = ready[:len(ready)-1]
		taken++
		for other := 1; other < 61; other++ {
			if after[k][other] {
				before[other]--
				if before[other] == 0 {
					ready = append(ready, other)
				}
			}
		}
	}
	return taken == 60
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1591)
	var grids [][][]int32
	for g := 0; g < 4000; g++ {
		order := make([]int32, 60)
		for i := range order {
			order[i] = int32(i + 1)
		}
		for i := 59; i >= 1; i-- {
			j := nextRandom(&seed) % int64(i+1)
			order[i], order[j] = order[j], order[i]
		}
		grid := make([][]int32, 60)
		for r := range grid {
			grid[r] = make([]int32, 60)
			for c := range grid[r] {
				grid[r][c] = order[0]
			}
		}
		for _, k := range order[1:] {
			r1, r2 := nextRandom(&seed)%60, nextRandom(&seed)%60
			c1, c2 := nextRandom(&seed)%60, nextRandom(&seed)%60
			for r := min(r1, r2); r <= max(r1, r2); r++ {
				for c := min(c1, c2); c <= max(c1, c2); c++ {
					grid[r][c] = k
				}
			}
		}
		if g%2 == 1 {
			r := nextRandom(&seed) % 60
			c := nextRandom(&seed) % 60
			grid[r][c] = int32(nextRandom(&seed)%60 + 1)
		}
		grids = append(grids, grid)
	}
	var check int64
	yes := 0
	for _, grid := range grids {
		ok := isPrintable(grid)
		var b int64
		if ok {
			yes++
			b = 1
		}
		check = (check*31 + b + 1) % 1000000007
	}
	fmt.Printf("4000 grids of 60 by 60: %d printable, checksum %d\n", yes, check)
}
