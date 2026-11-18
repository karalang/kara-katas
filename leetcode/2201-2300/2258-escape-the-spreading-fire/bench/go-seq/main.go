// LeetCode #2258: Escape the Spreading Fire -- Go mirror of the ★ arm:
// fire times by one breadth-first search from every fire, then a binary
// search over the wait, each wait tried by a breadth-first search of the
// person. Same workload and checksum as escape.kara.
package main

import "fmt"

const never int64 = 1000000000000

var steps = [4][2]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func fireTimes(grid [][]int64) [][]int64 {
	m, n := len(grid), len(grid[0])
	at := make([][]int64, m)
	queue := [][2]int{}
	for r := 0; r < m; r++ {
		at[r] = make([]int64, n)
		for c := 0; c < n; c++ {
			at[r][c] = never
			if grid[r][c] == 1 {
				at[r][c] = 0
				queue = append(queue, [2]int{r, c})
			}
		}
	}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head][0], queue[head][1]
		for _, s := range steps {
			nr, nc := r+s[0], c+s[1]
			if nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] == 0 && at[nr][nc] == never {
				at[nr][nc] = at[r][c] + 1
				queue = append(queue, [2]int{nr, nc})
			}
		}
	}
	return at
}

type state struct {
	r, c int
	t    int64
}

func escapes(grid [][]int64, fire [][]int64, wait int64) bool {
	m, n := len(grid), len(grid[0])
	if wait >= fire[0][0] {
		return false
	}
	seen := make([][]bool, m)
	for r := range seen {
		seen[r] = make([]bool, n)
	}
	seen[0][0] = true
	queue := []state{{0, 0, wait}}
	for head := 0; head < len(queue); head++ {
		q := queue[head]
		for _, s := range steps {
			nr, nc := q.r+s[0], q.c+s[1]
			if nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr][nc] != 0 || seen[nr][nc] {
				continue
			}
			if nr == m-1 && nc == n-1 {
				if q.t+1 <= fire[nr][nc] {
					return true
				}
				continue
			}
			if q.t+1 < fire[nr][nc] {
				seen[nr][nc] = true
				queue = append(queue, state{nr, nc, q.t + 1})
			}
		}
	}
	return false
}

func maximumMinutes(grid [][]int64) int64 {
	fire := fireTimes(grid)
	cells := int64(len(grid) * len(grid[0]))
	if !escapes(grid, fire, 0) {
		return -1
	}
	if escapes(grid, fire, cells) {
		return 1000000000
	}
	lo, hi := int64(0), cells
	for hi-lo > 1 {
		mid := (lo + hi) / 2
		if escapes(grid, fire, mid) {
			lo = mid
		} else {
			hi = mid
		}
	}
	return lo
}

func chase(seed *int64, m, n int, walls int64) [][]int64 {
	grid := make([][]int64, m)
	for r := 0; r < m; r++ {
		grid[r] = make([]int64, n)
		for c := 0; c < n; c++ {
			roll := nextRandom(seed) % 100
			if c == 1 && r > 0 {
				grid[r][c] = 2
			} else if c >= 2 && roll < walls {
				grid[r][c] = 2
			}
		}
	}
	grid[0][2] = 0
	grid[m-1][n-1] = 0
	grid[nextRandom(seed)%int64(m-1)+1][0] = 1
	return grid
}

func main() {
	seed := int64(2258)
	check, waits := int64(0), 0
	shapes := [3][2]int{{100, 200}, {200, 100}, {125, 160}}
	for t := 0; t < 300; t++ {
		m, n := shapes[t%3][0], shapes[t%3][1]
		answer := maximumMinutes(chase(&seed, m, n, 8))
		if answer >= 0 && answer < 1000000000 {
			waits++
		}
		check = (check*31 + answer + 1) % 1000000007
	}
	fmt.Printf("300 grids of 2 * 10^4 cells: %d with a wait, checksum %d\n", waits, check)
}
