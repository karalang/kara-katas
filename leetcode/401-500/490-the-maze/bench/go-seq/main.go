// Benchmark for #490: Go mirror of the ★ arm (breadth first over stopping
// cells); see ../the_maze.kara. The queue is a slice with a moving head.
package main

import "fmt"

func hasPath(maze [][]int64, start, destination []int64) bool {
	rows := int64(len(maze))
	cols := int64(len(maze[0]))
	seen := make([][]bool, rows)
	for i := range seen {
		seen[i] = make([]bool, cols)
	}
	type cell struct{ r, c int64 }
	queue := []cell{{start[0], start[1]}}
	seen[start[0]][start[1]] = true
	steps := [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for head := 0; head < len(queue); head++ {
		row, col := queue[head].r, queue[head].c
		if row == destination[0] && col == destination[1] {
			return true
		}
		for _, s := range steps {
			dr, dc := s[0], s[1]
			r, c := row, col
			for r+dr >= 0 && r+dr < rows && c+dc >= 0 && c+dc < cols && maze[r+dr][c+dc] == 0 {
				r += dr
				c += dc
			}
			if !seen[r][c] {
				seen[r][c] = true
				queue = append(queue, cell{r, c})
			}
		}
	}
	return false
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 60 mazes of 300 by 300 cells, a wall in each cell with odds of 1 in
	// 6, and a start and a destination on open cells, built once, then
	// each solved once.
	var n int64 = 300
	var mazes [][][]int64
	var starts, destinations [][]int64
	var seed int64 = 490
	for k := 0; k < 60; k++ {
		maze := make([][]int64, 0, n)
		for i := int64(0); i < n; i++ {
			line := make([]int64, 0, n)
			for j := int64(0); j < n; j++ {
				if nextRandom(&seed)%6 == 0 {
					line = append(line, 1)
				} else {
					line = append(line, 0)
				}
			}
			maze = append(maze, line)
		}
		start := []int64{nextRandom(&seed) % n, nextRandom(&seed) % n}
		destination := []int64{nextRandom(&seed) % n, nextRandom(&seed) % n}
		maze[start[0]][start[1]] = 0
		maze[destination[0]][destination[1]] = 0
		mazes = append(mazes, maze)
		starts = append(starts, start)
		destinations = append(destinations, destination)
	}
	reached := 0
	var checksum int64
	for k := range mazes {
		found := hasPath(mazes[k], starts[k], destinations[k])
		if found {
			reached++
		}
		add := int64(3)
		if found {
			add = 7
		}
		checksum = (checksum*31 + add) % 1000000007
	}
	fmt.Printf("60 mazes of 300 by 300: the destination reached in %d, checksum %d\n", reached, checksum)
}
