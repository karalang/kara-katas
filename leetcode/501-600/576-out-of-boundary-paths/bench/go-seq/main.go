// Benchmark for #576: Go mirror of the ★ arm (the ways forward, move by
// move); see ../find_paths.kara. A fresh grid of counts for every move,
// as the Kāra arm makes one.
package main

import "fmt"

func newGrid(m, n int64) [][]int64 {
	g := make([][]int64, m)
	for r := range g {
		g[r] = make([]int64, n)
	}
	return g
}

func findPaths(m, n, maxMove, startRow, startColumn int64) int64 {
	const modulus = 1000000007
	moves := [][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	ways := newGrid(m, n)
	ways[startRow][startColumn] = 1
	var out int64 = 0
	for k := int64(0); k < maxMove; k++ {
		next := newGrid(m, n)
		for r := int64(0); r < m; r++ {
			for c := int64(0); c < n; c++ {
				here := ways[r][c]
				if here == 0 {
					continue
				}
				for _, d := range moves {
					nr := r + d[0]
					nc := c + d[1]
					if nr < 0 || nr >= m || nc < 0 || nc >= n {
						out = (out + here) % modulus
					} else {
						next[nr][nc] = (next[nr][nc] + here) % modulus
					}
				}
			}
		}
		ways = next
	}
	return out
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var count int64 = 5000
	var seed int64 = 576
	var total int64 = 0
	var checksum int64 = 0
	for g := int64(0); g < count; g++ {
		m := 30 + nextRandom(&seed)%21
		n := 30 + nextRandom(&seed)%21
		maxMove := 30 + nextRandom(&seed)%21
		r := nextRandom(&seed) % m
		c := nextRandom(&seed) % n
		got := findPaths(m, n, maxMove, r, c)
		total = (total + got) % 1000000007
		checksum = (checksum*31 + got) % 1000000007
	}
	fmt.Printf("%d cases up to 50 by 50 and 50 moves: total %d, checksum %d\n", count, total, checksum)
}
