// Benchmark workload for LeetCode #329 — Go mirror of
// longest_increasing_path.kara.
//
// Same workload: a SIDE x SIDE grid built once, then PUNCHES punches, each
// replacing one cell and finding the longest increasing path again with a
// fresh memo.
package main

import "fmt"

const (
	SIDE    = 500
	PUNCHES = 20
	MODULUS = 1073741789
)

var steps = [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}

func longestFrom(matrix, memo [][]int64, r, c int64) int64 {
	if memo[r][c] > 0 {
		return memo[r][c]
	}
	rows := int64(len(matrix))
	cols := int64(len(matrix[0]))
	here := matrix[r][c]
	var best int64 = 1
	for _, s := range steps {
		nr := r + s[0]
		nc := c + s[1]
		if nr >= 0 && nr < rows && nc >= 0 && nc < cols && matrix[nr][nc] > here {
			l := 1 + longestFrom(matrix, memo, nr, nc)
			if l > best {
				best = l
			}
		}
	}
	memo[r][c] = best
	return best
}

func longestIncreasingPath(matrix [][]int64) int64 {
	if len(matrix) == 0 || len(matrix[0]) == 0 {
		return 0
	}
	memo := make([][]int64, len(matrix))
	for i, row := range matrix {
		memo[i] = make([]int64, len(row))
	}
	var best int64
	for r := int64(0); r < int64(len(matrix)); r++ {
		for c := int64(0); c < int64(len(matrix[0])); c++ {
			l := longestFrom(matrix, memo, r, c)
			if l > best {
				best = l
			}
		}
	}
	return best
}

var seed int64 = 329

func nextRand() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grid := make([][]int64, SIDE)
	for r := range grid {
		grid[r] = make([]int64, SIDE)
		for c := range grid[r] {
			grid[r][c] = nextRand() % 1000
		}
	}
	var sink int64
	for p := 0; p < PUNCHES; p++ {
		r := nextRand() % SIDE
		c := nextRand() % SIDE
		grid[r][c] = nextRand() % 1000
		l := longestIncreasingPath(grid)
		sink = (sink*31 + l*1000003 + r*SIDE + c) % MODULUS
	}
	fmt.Printf("sink %d\n", sink)
}
