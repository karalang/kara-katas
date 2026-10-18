// LeetCode #741: Cherry Pickup -- two walkers, one layer at a time.
// Benchmark mirror of the Kara star arm: two walkers go from the near
// corner to the far one together, a cherry on a shared cell counted
// once; keep the best cherries for every pair of rows after k steps
// and build the next layer from it.
package main

import "fmt"

func newLayer(n int) [][]int64 {
	var t [][]int64
	for r := 0; r < n; r++ {
		var row []int64
		for c := 0; c < n; c++ {
			row = append(row, -1)
		}
		t = append(t, row)
	}
	return t
}

func cherryPickup(grid [][]int64) int64 {
	n := len(grid)
	best := newLayer(n)
	if grid[0][0] == -1 {
		return 0
	}
	best[0][0] = grid[0][0]
	for k := 1; k < 2*n-1; k++ {
		next := newLayer(n)
		low, high := 0, k
		if k >= n {
			low = k - n + 1
			high = n - 1
		}
		for r1 := low; r1 <= high; r1++ {
			for r2 := low; r2 <= high; r2++ {
				c1, c2 := k-r1, k-r2
				if grid[r1][c1] == -1 || grid[r2][c2] == -1 {
					continue
				}
				from := int64(-1)
				for d1 := 0; d1 < 2; d1++ {
					for d2 := 0; d2 < 2; d2++ {
						p1, p2 := r1-d1, r2-d2
						if p1 >= 0 && p2 >= 0 && best[p1][p2] > from {
							from = best[p1][p2]
						}
					}
				}
				if from == -1 {
					continue
				}
				here := grid[r1][c1]
				if r2 != r1 {
					here += grid[r2][c2]
				}
				next[r1][r2] = from + here
			}
		}
		best = next
	}
	if best[n-1][n-1] == -1 {
		return 0
	}
	return best[n-1][n-1]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(741)
	n := int64(50)
	var grid [][]int64
	for r := int64(0); r < n; r++ {
		var row []int64
		for c := int64(0); c < n; c++ {
			corner := (r == 0 && c == 0) || (r == n-1 && c == n-1)
			if !corner && nextRandom(&seed)%10 == 0 {
				row = append(row, -1)
			} else {
				row = append(row, nextRandom(&seed)%2)
			}
		}
		grid = append(grid, row)
	}
	var total int64
	for round := 0; round < 300; round++ {
		for k := 0; k < 5; k++ {
			r := nextRandom(&seed) % n
			c := nextRandom(&seed) % n
			v := nextRandom(&seed) % 10
			corner := (r == 0 && c == 0) || (r == n-1 && c == n-1)
			if !corner {
				if v == 0 {
					grid[r][c] = -1
				} else {
					grid[r][c] = v % 2
				}
			}
		}
		total += cherryPickup(grid)
	}
	fmt.Printf("300 rounds of a 50 by 50 grid: %d cherries in all\n", total)
}
