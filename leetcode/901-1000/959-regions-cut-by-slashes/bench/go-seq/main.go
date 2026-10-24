// Benchmark: LeetCode #959 Regions Cut By Slashes -- the ★ arm, four
// triangles per cell, on grids of 30 by 30, LeetCode's largest. Mirrors
// regions_by_slashes.kara, .c, .rs and .py.
package main

import "fmt"

func find(parent []int, x int) int {
	r := x
	for parent[r] != r {
		r = parent[r]
	}
	for parent[x] != r {
		next := parent[x]
		parent[x] = r
		x = next
	}
	return r
}

func regionsBySlashes(grid []string) int {
	n := len(grid)
	parent := make([]int, 4*n*n)
	for i := range parent {
		parent[i] = i
	}
	sets := 4 * n * n
	union := func(a, b int) {
		ra, rb := find(parent, a), find(parent, b)
		if ra != rb {
			parent[ra] = rb
			sets--
		}
	}
	for r := 0; r < n; r++ {
		for c := 0; c < n; c++ {
			// triangles 0 top, 1 right, 2 bottom, 3 left
			t := 4 * (r*n + c)
			switch grid[r][c] {
			case ' ':
				union(t, t+1)
				union(t+1, t+2)
				union(t+2, t+3)
			case '/':
				union(t, t+3)
				union(t+1, t+2)
			default:
				union(t, t+1)
				union(t+2, t+3)
			}
			if c+1 < n {
				union(t+1, t+4+3)
			}
			if r+1 < n {
				union(t+2, t+4*n)
			}
		}
	}
	return sets
}

var seed int64 = 959

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomGrid(n int, blank int64) []string {
	grid := make([]string, n)
	for r := range grid {
		row := make([]byte, n)
		for c := range row {
			if nextRandom()%10 < blank {
				row[c] = ' '
			} else if nextRandom()%2 == 0 {
				row[c] = '/'
			} else {
				row[c] = '\\'
			}
		}
		grid[r] = string(row)
	}
	return grid
}

func main() {
	rounds := 300
	grids := make([][]string, 100)
	for i := range grids {
		grids[i] = randomGrid(30, int64(i%10))
	}
	total, check := 0, 0
	for r := 0; r < rounds; r++ {
		for i := 0; i < 100; i++ {
			k := regionsBySlashes(grids[(r+i)%100])
			total += k
			check = (check*31 + k + i) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 100 grids of 30 by 30: %d regions, checksum %d\n", rounds, total, check)
}
