// LeetCode #2852: Sum of Remoteness of All Cells -- the bench: the ★ arm
// over 20 grids of 300 x 300, LeetCode's most, values up to 10^6, a
// cell blocked from 1 time in 10 to 6 in 10, all drawn first, then each
// answered 10 times. The queue is a slice taken from the front.
package main

import "fmt"

type cell struct{ r, c int }

func sumRemoteness(grid [][]int64) int64 {
	n := len(grid)
	var total int64
	for _, row := range grid {
		for _, v := range row {
			if v > 0 {
				total += v
			}
		}
	}
	seen := make([][]bool, n)
	for i := range seen {
		seen[i] = make([]bool, n)
	}
	dirs := [4][2]int{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	var answer int64
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			if grid[i][j] < 0 || seen[i][j] {
				continue
			}
			seen[i][j] = true
			queue := []cell{{i, j}}
			var size, sum int64
			for len(queue) > 0 {
				p := queue[0]
				queue = queue[1:]
				size++
				sum += grid[p.r][p.c]
				for _, d := range dirs {
					nr, nc := p.r+d[0], p.c+d[1]
					if nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] > 0 && !seen[nr][nc] {
						seen[nr][nc] = true
						queue = append(queue, cell{nr, nc})
					}
				}
			}
			answer += size * (total - sum)
		}
	}
	return answer
}

var seed int64 = 2852

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 20, 10, 300
	grids := make([][][]int64, 0, count)
	for g := 0; g < count; g++ {
		blocked := nextRandom()%6 + 1
		grid := make([][]int64, n)
		for i := range grid {
			grid[i] = make([]int64, n)
			for j := range grid[i] {
				if nextRandom()%10 < blocked {
					grid[i][j] = -1
				} else {
					grid[i][j] = wide()%1000000 + 1
				}
			}
		}
		grids = append(grids, grid)
	}
	var check int64
	for r := int64(0); r < rounds; r++ {
		for _, grid := range grids {
			check = (check*31 + sumRemoteness(grid)%1000000007 + r) % 1000000007
		}
	}
	fmt.Printf("%d grids of %d x %d, %d rounds: checksum %d\n", count, n, n, rounds, check)
}
