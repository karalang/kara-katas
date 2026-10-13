// Benchmark for #529: Go mirror of the ★ arm (reveal recursively); see
// ../update_board.kara. The same seeded generator, so the same boards
// and clicks; a fresh copy of the board per click.
package main

import "fmt"

func minesAround(board [][]rune, r, c int64) int64 {
	var count int64
	for dr := int64(-1); dr <= 1; dr++ {
		for dc := int64(-1); dc <= 1; dc++ {
			y, x := r+dr, c+dc
			if (dr != 0 || dc != 0) && y >= 0 && y < int64(len(board)) && x >= 0 && x < int64(len(board[0])) {
				if v := board[y][x]; v == 'M' || v == 'X' {
					count++
				}
			}
		}
	}
	return count
}

func reveal(board [][]rune, r, c int64) {
	if board[r][c] != 'E' {
		return
	}
	count := minesAround(board, r, c)
	if count > 0 {
		board[r][c] = rune(48 + count)
		return
	}
	board[r][c] = 'B'
	for dr := int64(-1); dr <= 1; dr++ {
		for dc := int64(-1); dc <= 1; dc++ {
			y, x := r+dr, c+dc
			if y >= 0 && y < int64(len(board)) && x >= 0 && x < int64(len(board[0])) {
				reveal(board, y, x)
			}
		}
	}
}

func updateBoard(board [][]rune, click []int64) [][]rune {
	r, c := click[0], click[1]
	if board[r][c] == 'M' {
		board[r][c] = 'X'
	} else {
		reveal(board, r, c)
	}
	return board
}

func clone(board [][]rune) [][]rune {
	out := make([][]rune, len(board))
	for i, row := range board {
		out[i] = append([]rune(nil), row...)
	}
	return out
}

func main() {
	var seed int64 = 529
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	var boards [][][]rune
	for b := 0; b < 50; b++ {
		percent := nextRandom() % 21
		var board [][]rune
		for i := 0; i < 50; i++ {
			var row []rune
			for j := 0; j < 50; j++ {
				if nextRandom()%100 < percent {
					row = append(row, 'M')
				} else {
					row = append(row, 'E')
				}
			}
			board = append(board, row)
		}
		boards = append(boards, board)
	}
	var opened, exploded, checksum int64
	for round := 0; round < 400; round++ {
		for b := range boards {
			r := nextRandom() % 50
			c := nextRandom() % 50
			after := updateBoard(clone(boards[b]), []int64{r, c})
			var shown int64
			for _, row := range after {
				for _, ch := range row {
					if ch == 'X' {
						exploded++
					} else if ch != 'E' && ch != 'M' {
						shown++
					}
				}
			}
			opened += shown
			checksum = (checksum*31 + shown) % 1000000007
		}
	}
	fmt.Printf("50 boards of 50 by 50, 400 rounds of clicks: %d opened, %d exploded, checksum %d\n", opened, exploded, checksum)
}
