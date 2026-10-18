// LeetCode #694: Number of Distinct Islands -- bench program, Go mirror of the union-find arm.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 694

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

// Lexicographic, a shorter prefix first, as Vec[i64] compares.
func less(a, b []int64) bool {
	for i := 0; i < len(a) && i < len(b); i++ {
		if a[i] != b[i] {
			return a[i] < b[i]
		}
	}
	return len(a) < len(b)
}

func equal(a, b []int64) bool {
	return !less(a, b) && !less(b, a)
}

func numDistinctIslands(grid [][]int64) int64 {
	m, n := len(grid), len(grid[0])
	parent := make([]int, m*n)
	for i := range parent {
		parent[i] = i
	}
	for r := 0; r < m; r++ {
		for c := 0; c < n; c++ {
			if grid[r][c] == 0 {
				continue
			}
			if r+1 < m && grid[r+1][c] == 1 {
				a := find(parent, r*n+c)
				b := find(parent, (r+1)*n+c)
				parent[a] = b
			}
			if c+1 < n && grid[r][c+1] == 1 {
				a := find(parent, r*n+c)
				b := find(parent, r*n+c+1)
				parent[a] = b
			}
		}
	}
	first := make([]int, m*n)
	slot := make([]int, m*n)
	for i := range first {
		first[i] = -1
	}
	shapes := [][]int64{}
	for r := 0; r < m; r++ {
		for c := 0; c < n; c++ {
			if grid[r][c] == 0 {
				continue
			}
			root := find(parent, r*n+c)
			if first[root] < 0 {
				first[root] = r*n + c
				slot[root] = len(shapes)
				shapes = append(shapes, []int64{})
			}
			r0, c0 := first[root]/n, first[root]%n
			shapes[slot[root]] = append(shapes[slot[root]], int64(r-r0)*200+int64(c-c0))
		}
	}
	sort.Slice(shapes, func(i, j int) bool { return less(shapes[i], shapes[j]) })
	var distinct int64
	for i := range shapes {
		if i == 0 || !equal(shapes[i], shapes[i-1]) {
			distinct++
		}
	}
	return distinct
}

func main() {
	grids := [][][]int64{}
	for g := 0; g < 40; g++ {
		percent := 30 + nextRandom()%31
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
	rounds := 150
	var total, checksum int64
	for k := 0; k < rounds; k++ {
		for _, grid := range grids {
			r := numDistinctIslands(grid)
			total += r
			checksum = (checksum*31 + r) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 40 grids of 50 by 50: %d distinct islands counted, checksum %d\n", rounds, total, checksum)
}
