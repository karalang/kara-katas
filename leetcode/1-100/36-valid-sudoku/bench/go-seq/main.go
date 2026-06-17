// LeetCode #36 bench — Go (mirror of valid_sudoku.kara).
//
// Single-pass bitmask validation of a 9x9 board with three stack [9]int64 mask
// arrays, perturb-validate-restore TOTAL times with the verdict folded into a
// checksum (single goroutine — seq).
package main

import "fmt"

func boxIndex(r, c int64) int64 {
	return (r/3)*3 + c/3
}

func isValid(board []int64) bool {
	var rows, cols, boxes [9]int64
	for r := int64(0); r < 9; r++ {
		for c := int64(0); c < 9; c++ {
			d := board[r*9+c]
			if d != 0 {
				bit := int64(1) << d
				b := boxIndex(r, c)
				if (rows[r]&bit) != 0 || (cols[c]&bit) != 0 || (boxes[b]&bit) != 0 {
					return false
				}
				rows[r] |= bit
				cols[c] |= bit
				boxes[b] |= bit
			}
		}
	}
	return true
}

func main() {
	const total int64 = 5000000
	const modulus int64 = 1000000007

	board := [81]int64{
		5, 3, 4, 6, 7, 8, 9, 1, 2, 6, 7, 2, 1, 9, 5, 3, 4, 8, 1, 9, 8, 3, 4, 2, 5, 6, 7, 8, 5, 9,
		7, 6, 1, 4, 2, 3, 4, 2, 6, 8, 5, 3, 7, 9, 1, 7, 1, 3, 9, 2, 4, 8, 5, 6, 9, 6, 1, 5, 3, 7,
		2, 8, 4, 2, 8, 7, 4, 1, 9, 6, 3, 5, 3, 4, 5, 2, 8, 6, 1, 7, 9,
	}

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		pos := k % 81
		digit := (k % 9) + 1
		save := board[pos]
		board[pos] = digit
		var v int64 = 0
		if isValid(board[:]) {
			v = 1
		}
		acc = (acc*31 + v) % modulus
		board[pos] = save
	}

	fmt.Println(acc)
}
