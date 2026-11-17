// LeetCode #2257: Count Unguarded Cells in the Grid -- the benchmark's Go
// mirror of unguarded.kara: a grid of marks and a walk from every guard in
// each of the four directions until a wall, a guard or the edge.
package main

import "fmt"

// 0 empty, 1 seen, 2 guard, 3 wall
func countUnguarded(m, n int64, guards, walls [][2]int64) int64 {
	grid := make([][]uint8, m)
	for r := range grid {
		grid[r] = make([]uint8, n)
	}
	for _, g := range guards {
		grid[g[0]][g[1]] = 2
	}
	for _, w := range walls {
		grid[w[0]][w[1]] = 3
	}
	dirs := [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for _, g := range guards {
		for _, d := range dirs {
			r, c := g[0]+d[0], g[1]+d[1]
			for r >= 0 && r < m && c >= 0 && c < n && grid[r][c] < 2 {
				grid[r][c] = 1
				r += d[0]
				c += d[1]
			}
		}
	}
	var count int64
	for _, row := range grid {
		for _, cell := range row {
			if cell == 0 {
				count++
			}
		}
	}
	return count
}

var seed int64 = 2257

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func place(m, n int64, guards, walls int) ([][2]int64, [][2]int64) {
	taken := make([]bool, m*n)
	cells := make([][2]int64, 0, guards+walls)
	for len(cells) < guards+walls {
		k := wideRandom() % (m * n)
		if !taken[k] {
			taken[k] = true
			cells = append(cells, [2]int64{k / n, k % n})
		}
	}
	return cells[:guards], cells[guards:]
}

func main() {
	shapes := [3][2]int64{{1, 100000}, {250, 400}, {100000, 1}}
	var check int64
	for t := 0; t < 300; t++ {
		m, n := shapes[t%3][0], shapes[t%3][1]
		guards, walls := place(m, n, 2000, 10000)
		check = (check*31 + countUnguarded(m, n, guards, walls) + 1) % 1000000007
	}
	fmt.Printf("300 grids of 10^5 cells: checksum %d\n", check)
}
