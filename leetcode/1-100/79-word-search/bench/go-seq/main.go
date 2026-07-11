// Benchmark workload — Word Search (LeetCode #79).
// Go mirror of ../word_search.kara. Enumerates every self-avoiding walk (up to
// depth steps) from every start cell of a fixed all-'A' 5x5 board and folds each
// visited cell into a threaded accumulator — the 4-neighbour, in-place mark/restore
// DFS backtracking that powers word search, with the letter-match replaced by
// "any unvisited cell, up to depth" so every branch is taken. K=12 iterations
// seeded by the iteration index. The DFS recursion is the measured work.
package main

import "fmt"

const rows = 5
const cols = 5

// Nested heap board ([][]uint8) — the same pointer-chased, bounds-checked layout
// Kara's Vec[Vec[u8]] uses, so the comparison measures the DFS on an equal data
// structure rather than a fixed 2D array's locality advantage.
func walk(board [][]uint8, r, c, depth, acc int64) int64 {
	if r < 0 || r >= rows || c < 0 || c >= cols {
		return acc
	}
	if board[r][c] == 0 {
		return acc
	}
	a := (acc*131 + (r*cols + c) + 1) % 1000000007
	if depth == 0 {
		return a
	}
	saved := board[r][c]
	board[r][c] = 0
	a = walk(board, r+1, c, depth-1, a)
	a = walk(board, r-1, c, depth-1, a)
	a = walk(board, r, c+1, depth-1, a)
	a = walk(board, r, c-1, depth-1, a)
	board[r][c] = saved
	return a
}

func searchAll(board [][]uint8, depth, seed int64) int64 {
	a := seed
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			a = walk(board, r, c, depth, a)
		}
	}
	return a
}

func main() {
	const depth = 25
	const total = 12
	const modulus = 1000000007
	board := make([][]uint8, rows)
	for r := 0; r < rows; r++ {
		board[r] = make([]uint8, cols)
		for c := 0; c < cols; c++ {
			board[r][c] = 'A'
		}
	}
	var sum int64 = 0
	for iter := int64(0); iter < total; iter++ {
		rr := searchAll(board, depth, iter)
		sum = (sum + rr) % modulus
	}
	fmt.Println(sum)
}
