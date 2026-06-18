// LeetCode #37 bench — Go (mirror of sudoku_solver.kara).
//
// Bitmask backtracking solver over a flat []int64 board with three stack [9]int64 mask
// arrays, linear cell order, ascending digit order, XOR undo. Workload: TOTAL times
// copy the "world's hardest sudoku" template, clear cell k%81, solve in place, fold a
// position-weighted signature of the solved grid into a checksum (single goroutine — seq).
package main

import "fmt"

func boxIndex(r, c int64) int64 {
	return (r/3)*3 + c/3
}

func goSolve(board []int64, rows, cols, boxes []int64, pos int64) bool {
	if pos == 81 {
		return true
	}
	r := pos / 9
	c := pos % 9
	if board[pos] != 0 {
		return goSolve(board, rows, cols, boxes, pos+1)
	}
	b := boxIndex(r, c)
	used := rows[r] | cols[c] | boxes[b]
	for d := int64(1); d <= 9; d++ {
		bit := int64(1) << d
		if (used & bit) == 0 {
			board[pos] = d
			rows[r] |= bit
			cols[c] |= bit
			boxes[b] |= bit
			if goSolve(board, rows, cols, boxes, pos+1) {
				return true
			}
			board[pos] = 0
			rows[r] ^= bit
			cols[c] ^= bit
			boxes[b] ^= bit
		}
	}
	return false
}

func solve(board []int64) bool {
	var rows, cols, boxes [9]int64
	for i := int64(0); i < 81; i++ {
		d := board[i]
		if d != 0 {
			r := i / 9
			c := i % 9
			bit := int64(1) << d
			rows[r] |= bit
			cols[c] |= bit
			boxes[boxIndex(r, c)] |= bit
		}
	}
	return goSolve(board, rows[:], cols[:], boxes[:], 0)
}

func main() {
	const total int64 = 500
	const modulus int64 = 1000000007

	template := [81]int64{
		8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 0, 0, 0, 7, 0, 0, 9, 0, 2, 0, 0,
		0, 5, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 4, 5, 7, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0,
		0, 0, 1, 0, 0, 0, 0, 6, 8, 0, 0, 8, 5, 0, 0, 0, 1, 0, 0, 9, 0, 0, 0, 0, 4, 0, 0,
	}

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		var work [81]int64
		for j := int64(0); j < 81; j++ {
			work[j] = template[j]
		}
		work[k%81] = 0

		solve(work[:])

		var sig int64 = 0
		for i := int64(0); i < 81; i++ {
			sig += work[i] * (i + 1)
		}
		acc = (acc*31 + sig) % modulus
	}

	fmt.Println(acc)
}
