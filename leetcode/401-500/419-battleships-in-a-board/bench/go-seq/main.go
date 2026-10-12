// LeetCode #419: Battleships in a Board -- Go mirror of battleships.kara
// (count the first cells). Cells are runes, as Kāra's are chars.
package main

import "fmt"

func countBattleships(board [][]rune) int64 {
	var count int64
	for r := range board {
		for c := range board[r] {
			if board[r][c] == 'X' && (r == 0 || board[r-1][c] != 'X') && (c == 0 || board[r][c-1] != 'X') {
				count++
			}
		}
	}
	return count
}

var seed int64 = 419

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func clear(board [][]rune, r, c int64) bool {
	n := int64(len(board))
	around := [5][2]int64{{r, c}, {r - 1, c}, {r + 1, c}, {r, c - 1}, {r, c + 1}}
	for _, p := range around {
		if p[0] >= 0 && p[0] < n && p[1] >= 0 && p[1] < n && board[p[0]][p[1]] == 'X' {
			return false
		}
	}
	return true
}

func main() {
	var n int64 = 200
	rounds := 20000
	board := make([][]rune, n)
	for r := range board {
		board[r] = make([]rune, n)
		for c := range board[r] {
			board[r][c] = '.'
		}
	}
	for t := 0; t < 4000; t++ {
		length := 1 + step()%4
		across := step()%2 == 0
		r := step() % n
		c := step() % n
		var dr, dc int64 = 1, 0
		if across {
			dr, dc = 0, 1
		}
		fits := r+dr*(length-1) < n && c+dc*(length-1) < n
		for k := int64(0); k < length; k++ {
			if fits && !clear(board, r+dr*k, c+dc*k) {
				fits = false
			}
		}
		if fits {
			for k := int64(0); k < length; k++ {
				board[r+dr*k][c+dc*k] = 'X'
			}
		}
	}
	var total, checksum int64
	for i := 0; i < rounds; i++ {
		r := step() % n
		c := step() % n
		if board[r][c] == 'X' {
			board[r][c] = '.'
			if !clear(board, r, c) {
				board[r][c] = 'X'
			}
		} else if clear(board, r, c) {
			board[r][c] = 'X'
		}
		answer := countBattleships(board)
		total += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d rounds on a %dx%d board: total %d, checksum %d\n", rounds, n, n, total, checksum)
}
