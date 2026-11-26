// LeetCode #1765: Map of Highest Peak -- the bench in Go, mirroring
// highest_peak.kara: a breadth-first search from every water cell at once,
// the queue a slice read from its head.
package main

import "fmt"

type cell struct{ r, c int64 }

func highestPeak(isWater [][]int32) [][]int32 {
	rows, cols := int64(len(isWater)), int64(len(isWater[0]))
	height := make([][]int32, rows)
	for r := range height {
		height[r] = make([]int32, cols)
		for c := range height[r] {
			height[r][c] = -1
		}
	}
	var queue []cell
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			if isWater[r][c] == 1 {
				height[r][c] = 0
				queue = append(queue, cell{r, c})
			}
		}
	}
	dirs := [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head].r, queue[head].c
		for _, d := range dirs {
			nr, nc := r+d[0], c+d[1]
			if nr >= 0 && nr < rows && nc >= 0 && nc < cols && height[nr][nc] == -1 {
				height[nr][nc] = height[r][c] + 1
				queue = append(queue, cell{nr, nc})
			}
		}
	}
	return height
}

var seed int64 = 1765

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const size = 800
	grid := make([][]int32, size)
	for r := range grid {
		grid[r] = make([]int32, size)
		for c := range grid[r] {
			if nextRandom()%5000 == 0 {
				grid[r][c] = 1
			}
		}
	}
	grid[0][0] = 1
	var check int64
	for call := int64(0); call < 100; call++ {
		r := (check + call*7919) % size
		c := (check/7 + call*104729) % size
		grid[r][c] = 1 - grid[r][c]
		grid[0][0] = 1
		height := highestPeak(grid)
		check = (check*31 + int64(height[c][r]) + int64(height[size-1-r][size-1-c])) % 1000000007
	}
	fmt.Printf("100 calls on 800 by 800: checksum %d\n", check)
}
