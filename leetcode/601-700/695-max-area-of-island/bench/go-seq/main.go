// LeetCode #695: Max Area of Island -- bench program, Go mirror of the union-find arm.
package main

import "fmt"

var seed int64 = 695

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func find(parent []int, x int) int {
	root := x
	for parent[root] != root {
		root = parent[root]
	}
	for parent[x] != root {
		next := parent[x]
		parent[x] = root
		x = next
	}
	return root
}

func join(parent []int, size []int64, a, b int) {
	x, y := find(parent, a), find(parent, b)
	if x == y {
		return
	}
	if size[x] < size[y] {
		x, y = y, x
	}
	parent[y] = x
	size[x] += size[y]
}

func maxAreaOfIsland(grid [][]int64) int64 {
	m, n := len(grid), len(grid[0])
	parent := make([]int, m*n)
	size := make([]int64, m*n)
	for i := range parent {
		parent[i] = i
		size[i] = 1
	}
	for r := 0; r < m; r++ {
		for c := 0; c < n; c++ {
			if grid[r][c] == 0 {
				continue
			}
			if r+1 < m && grid[r+1][c] == 1 {
				join(parent, size, r*n+c, (r+1)*n+c)
			}
			if c+1 < n && grid[r][c+1] == 1 {
				join(parent, size, r*n+c, r*n+c+1)
			}
		}
	}
	var best int64
	for r := 0; r < m; r++ {
		for c := 0; c < n; c++ {
			if grid[r][c] == 1 && find(parent, r*n+c) == r*n+c && size[r*n+c] > best {
				best = size[r*n+c]
			}
		}
	}
	return best
}

func main() {
	grids := [][][]int64{}
	for g := 0; g < 40; g++ {
		percent := 30 + nextRandom()%41
		grid := [][]int64{}
		for r := 0; r < 50; r++ {
			line := []int64{}
			for c := 0; c < 50; c++ {
				v := int64(0)
				if nextRandom()%100 < percent {
					v = 1
				}
				line = append(line, v)
			}
			grid = append(grid, line)
		}
		grids = append(grids, grid)
	}
	rounds := 300
	var total, checksum int64
	for k := 0; k < rounds; k++ {
		for _, grid := range grids {
			r := maxAreaOfIsland(grid)
			total += r
			checksum = (checksum*31 + r) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 40 grids of 50 by 50: largest areas sum to %d, checksum %d\n", rounds, total, checksum)
}
