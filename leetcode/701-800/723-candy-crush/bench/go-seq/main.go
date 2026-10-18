// LeetCode #723: Candy Crush -- crushed cells marked by their sign.
// Benchmark mirror of the Kara star arm: each round marks every run of
// three across or down by negating its cells, then drops each column,
// until a round marks nothing; the board is crushed on a copy.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func candyCrush(board [][]int64) [][]int64 {
	m, n := len(board), len(board[0])
	b := make([][]int64, m)
	for r := range board {
		b[r] = append([]int64(nil), board[r]...)
	}
	stable := false
	for !stable {
		stable = true
		for r := 0; r < m; r++ {
			for c := 0; c < n-2; c++ {
				v := abs(b[r][c])
				if v != 0 && abs(b[r][c+1]) == v && abs(b[r][c+2]) == v {
					b[r][c], b[r][c+1], b[r][c+2] = -v, -v, -v
					stable = false
				}
			}
		}
		for r := 0; r < m-2; r++ {
			for c := 0; c < n; c++ {
				v := abs(b[r][c])
				if v != 0 && abs(b[r+1][c]) == v && abs(b[r+2][c]) == v {
					b[r][c], b[r+1][c], b[r+2][c] = -v, -v, -v
					stable = false
				}
			}
		}
		for c := 0; c < n; c++ {
			write := m - 1
			for r := m - 1; r >= 0; r-- {
				if b[r][c] > 0 {
					b[write][c] = b[r][c]
					write--
				}
			}
			for ; write >= 0; write-- {
				b[write][c] = 0
			}
		}
	}
	return b
}

func main() {
	seed := int64(723)
	var boards [][][]int64
	for d := 0; d < 40; d++ {
		board := make([][]int64, 50)
		for r := range board {
			board[r] = make([]int64, 50)
			for c := range board[r] {
				board[r][c] = 1 + nextRandom(&seed)%5
			}
		}
		boards = append(boards, board)
	}
	sum := 0
	for round := int64(0); round < 100; round++ {
		for d := int64(0); d < 40; d++ {
			r, c := (round*7+d)%50, (round*13+d*3)%50
			boards[d][r][c] = 1 + (boards[d][r][c]+round)%5
			after := candyCrush(boards[d])
			for _, row := range after {
				for _, v := range row {
					if v == 0 {
						sum++
					}
				}
			}
		}
	}
	fmt.Printf("100 rounds of 40 boards of 50 x 50: %d empty cells\n", sum)
}
