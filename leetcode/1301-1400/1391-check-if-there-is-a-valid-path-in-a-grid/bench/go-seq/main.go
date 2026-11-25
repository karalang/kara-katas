// LeetCode #1391 bench, Go mirror of the ★ arm: the queue a slice read
// from a moving head.
package main

import "fmt"

type cell struct{ r, c int64 }

var ways = [][]cell{
	{},
	{{0, -1}, {0, 1}},
	{{-1, 0}, {1, 0}},
	{{0, -1}, {1, 0}},
	{{0, 1}, {1, 0}},
	{{0, -1}, {-1, 0}},
	{{0, 1}, {-1, 0}},
}

func opens(street int32, dr, dc int64) bool {
	for _, w := range ways[street] {
		if w.r == dr && w.c == dc {
			return true
		}
	}
	return false
}

func hasValidPath(grid [][]int32) bool {
	m := int64(len(grid))
	n := int64(len(grid[0]))
	seen := make([]bool, m*n)
	queue := []cell{{0, 0}}
	seen[0] = true
	for head := 0; head < len(queue); head++ {
		r, c := queue[head].r, queue[head].c
		if r == m-1 && c == n-1 {
			return true
		}
		for _, w := range ways[grid[r][c]] {
			nr, nc := r+w.r, c+w.c
			if nr < 0 || nr >= m || nc < 0 || nc >= n || seen[nr*n+nc] {
				continue
			}
			if opens(grid[nr][nc], -w.r, -w.c) {
				seen[nr*n+nc] = true
				queue = append(queue, cell{nr, nc})
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
	const m, n = 299, 300
	grid := make([][]int32, m)
	for r := range grid {
		grid[r] = make([]int32, n)
		for c := range grid[r] {
			grid[r][c] = 1
		}
	}
	for r := 0; r < m-1; r++ {
		if r%2 == 0 {
			grid[r][n-1] = 3
			grid[r+1][n-1] = 5
		} else {
			grid[r][0] = 4
			grid[r+1][0] = 6
		}
	}
	var seed int64 = 1391
	var check int64
	whole := hasValidPath(grid)
	for round := 0; round < 3000; round++ {
		seed = (seed + check) % 2147483648
		cell := nextRandom(&seed) % (m * n)
		r, c := cell/n, cell%n
		street := grid[r][c]
		grid[r][c] = street%6 + 1
		got := hasValidPath(grid)
		grid[r][c] = street
		var g int64 = 1
		if got {
			g = 2
		}
		check = (check*131 + g*(cell+1)) % 1000000007
	}
	fmt.Printf("3000 rounds over a 299 by 300 snake, whole %t: checksum %d\n", whole, check)
}
