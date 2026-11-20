// LeetCode #1730: Shortest Path to Get Food -- the bench (food.kara): a
// breadth-first search from you, the first food off the queue the
// nearest.
package main

import "fmt"

func getFood(grid [][]byte) int32 {
	rows, cols := len(grid), len(grid[0])
	distance := make([][]int32, rows)
	queue := make([][2]int, 0)
	for r := range distance {
		distance[r] = make([]int32, cols)
		for c := range distance[r] {
			distance[r][c] = -1
			if grid[r][c] == '*' {
				distance[r][c] = 0
				queue = append(queue, [2]int{r, c})
			}
		}
	}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head][0], queue[head][1]
		if grid[r][c] == '#' {
			return distance[r][c]
		}
		for _, d := range [4][2]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}} {
			nr, nc := r+d[0], c+d[1]
			if nr < 0 || nr >= rows || nc < 0 || nc >= cols {
				continue
			}
			if grid[nr][nc] != 'X' && distance[nr][nc] < 0 {
				distance[nr][nc] = distance[r][c] + 1
				queue = append(queue, [2]int{nr, nc})
			}
		}
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 10
	var rounds int64 = 200
	side := 200
	var seed int64 = 1730
	problems := make([][][]byte, count)
	for p := range problems {
		grid := make([][]byte, side)
		for r := range grid {
			grid[r] = make([]byte, side)
			for c := range grid[r] {
				x := nextRandom(&seed) % 20000
				if x < 5000 {
					grid[r][c] = 'X'
				} else if x < 5001 {
					grid[r][c] = '#'
				} else {
					grid[r][c] = 'O'
				}
			}
		}
		at := int(nextRandom(&seed) % int64(side*side))
		grid[at/side][at%side] = '*'
		problems[p] = grid
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, grid := range problems {
			answer := int64(getFood(grid))
			sum += answer
			check = (check*31 + answer + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d grids of %d by %d, %d rounds: answers sum to %d, checksum %d\n", count, side, side, rounds, sum, check)
}
