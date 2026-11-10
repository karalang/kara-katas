// Benchmark: LeetCode #1091 Shortest Path in Binary Matrix -- Go mirror of
// the ★ arm: breadth-first search with a slice used as a queue and a grid of
// distances. Same workload and sink as ../shortest_path_binary_matrix.kara.
package main

import "fmt"

type cell struct{ r, c int64 }

func shortestPathBinaryMatrix(grid [][]int64) int64 {
	n := int64(len(grid))
	if grid[0][0] == 1 || grid[n-1][n-1] == 1 {
		return -1
	}
	dist := make([][]int64, n)
	for i := range dist {
		dist[i] = make([]int64, n)
		for j := range dist[i] {
			dist[i][j] = -1
		}
	}
	dist[0][0] = 1
	queue := []cell{{0, 0}}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head].r, queue[head].c
		if r == n-1 && c == n-1 {
			return dist[r][c]
		}
		for dr := int64(-1); dr <= 1; dr++ {
			for dc := int64(-1); dc <= 1; dc++ {
				nr, nc := r+dr, c+dc
				if nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 0 && dist[nr][nc] == -1 {
					dist[nr][nc] = dist[r][c] + 1
					queue = append(queue, cell{nr, nc})
				}
			}
		}
	}
	return -1
}

var seed int64 = 1091

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grids := make([][][]int64, 0)
	for k := int64(0); k < 200; k++ {
		blocked := 25 + k%20
		grid := make([][]int64, 100)
		for r := range grid {
			grid[r] = make([]int64, 100)
			for c := range grid[r] {
				if nextRandom()%100 < blocked {
					grid[r][c] = 1
				}
			}
		}
		grid[0][0] = 0
		grid[99][99] = 0
		grids = append(grids, grid)
	}
	var none, total, check int64
	for round := 0; round < 20; round++ {
		for _, grid := range grids {
			answer := shortestPathBinaryMatrix(grid)
			if answer == -1 {
				none++
			} else {
				total += answer
			}
			check = (check*31 + answer + 1) % 1000000007
		}
	}
	fmt.Printf("20 rounds over 200 grids of 100 by 100: %d without a path, lengths sum to %d, checksum %d\n", none, total, check)
}
