// LeetCode #2812: Find the Safest Path in a Grid -- the bench in Go: the
// ★ arm over 10 grids of 400 by 400, a thief in about one cell of 2000,
// all drawn first, then each answered 3 times. The queues are slices
// read from a head index.
package main

import "fmt"

var dirs = [4][2]int64{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}

type cell struct{ r, c int64 }

func thiefDistances(grid [][]int64) [][]int64 {
	n := int64(len(grid))
	dist := make([][]int64, n)
	queue := []cell{}
	for r := int64(0); r < n; r++ {
		dist[r] = make([]int64, n)
		for c := int64(0); c < n; c++ {
			dist[r][c] = -1
			if grid[r][c] == 1 {
				dist[r][c] = 0
				queue = append(queue, cell{r, c})
			}
		}
	}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head].r, queue[head].c
		for _, d := range dirs {
			nr, nc := r+d[0], c+d[1]
			if nr >= 0 && nr < n && nc >= 0 && nc < n && dist[nr][nc] == -1 {
				dist[nr][nc] = dist[r][c] + 1
				queue = append(queue, cell{nr, nc})
			}
		}
	}
	return dist
}

func reachable(dist [][]int64, s int64) bool {
	n := int64(len(dist))
	if dist[0][0] < s {
		return false
	}
	seen := make([][]bool, n)
	for r := range seen {
		seen[r] = make([]bool, n)
	}
	seen[0][0] = true
	queue := []cell{{0, 0}}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head].r, queue[head].c
		if r == n-1 && c == n-1 {
			return true
		}
		for _, d := range dirs {
			nr, nc := r+d[0], c+d[1]
			if nr >= 0 && nr < n && nc >= 0 && nc < n && !seen[nr][nc] && dist[nr][nc] >= s {
				seen[nr][nc] = true
				queue = append(queue, cell{nr, nc})
			}
		}
	}
	return false
}

func maximumSafenessFactor(grid [][]int64) int64 {
	n := len(grid)
	dist := thiefDistances(grid)
	lo := int64(0)
	hi := min(dist[0][0], dist[n-1][n-1])
	for lo < hi {
		mid := (lo + hi + 1) / 2
		if reachable(dist, mid) {
			lo = mid
		} else {
			hi = mid - 1
		}
	}
	return lo
}

var seed int64 = 2812

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 10, 3
	var n int64 = 400
	grids := make([][][]int64, count)
	for g := range grids {
		grid := make([][]int64, n)
		for r := range grid {
			grid[r] = make([]int64, n)
			for c := range grid[r] {
				if nextRandom()%2000 == 0 {
					grid[r][c] = 1
				}
			}
		}
		r := nextRandom() % n
		c := nextRandom() % n
		grid[r][c] = 1
		grids[g] = grid
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, grid := range grids {
			a := maximumSafenessFactor(grid)
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d grids of %d, %d rounds: safeness sums to %d, checksum %d\n", count, n, rounds, total, check)
}
