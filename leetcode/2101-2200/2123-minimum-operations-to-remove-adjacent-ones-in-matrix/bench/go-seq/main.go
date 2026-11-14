// LeetCode #2123: Minimum Operations to Remove Adjacent Ones in Matrix --
// the benchmark, the same algorithm as isolated.kara: the ones a bipartite
// graph by the parity of row plus column, the answer a maximum matching
// grown by Kuhn's augmenting paths.

package main

import "fmt"

func tryMatch(u int, adj [][]int, partner, seen []int, stamp int) bool {
	for _, v := range adj[u] {
		if seen[v] == stamp {
			continue
		}
		seen[v] = stamp
		if partner[v] < 0 || tryMatch(partner[v], adj, partner, seen, stamp) {
			partner[v] = u
			return true
		}
	}
	return false
}

func minimumOperations(grid [][]int) int {
	rows, cols := len(grid), len(grid[0])
	adj := make([][]int, rows*cols)
	steps := [4][2]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if grid[r][c] == 0 || (r+c)%2 != 0 {
				continue
			}
			for _, s := range steps {
				nr, nc := r+s[0], c+s[1]
				if nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 1 {
					adj[r*cols+c] = append(adj[r*cols+c], nr*cols+nc)
				}
			}
		}
	}
	partner := make([]int, rows*cols)
	seen := make([]int, rows*cols)
	for i := range partner {
		partner[i], seen[i] = -1, -1
	}
	matched := 0
	for u := 0; u < rows*cols; u++ {
		if len(adj[u]) > 0 && tryMatch(u, adj, partner, seen, u) {
			matched++
		}
	}
	return matched
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2123)
	grids := make([][][]int, 0, 12)
	for g := 0; g < 12; g++ {
		chance := int64([]int{1, 2, 3}[g%3])
		grid := make([][]int, 300)
		for r := range grid {
			grid[r] = make([]int, 300)
			for c := range grid[r] {
				if nextRandom(&seed)%4 < chance {
					grid[r][c] = 1
				}
			}
		}
		grids = append(grids, grid)
	}
	var total, check int64
	for round := 0; round < 10; round++ {
		for g := 0; g < 12; g++ {
			cell := (round*7919 + g*104729) % 90000
			grids[g][cell/300][cell%300] = 1 - grids[g][cell/300][cell%300]
			got := int64(minimumOperations(grids[g]))
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("120 solves: %d operations, checksum %d\n", total, check)
}
