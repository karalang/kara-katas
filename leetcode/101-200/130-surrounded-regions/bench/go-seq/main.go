// Benchmark harness for LeetCode #130 — Surrounded Regions.
// Mirrors surrounded_regions.kara algorithm-for-algorithm, including the
// nested [][]int64 board and the explicit position stack.
package main

import "fmt"

func flood(board [][]int64, rows int64, cols int64, sr int64, sc int64) {
	stack := make([]int64, 0, 64)
	stack = append(stack, sr*cols+sc)
	for len(stack) > 0 {
		pos := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		r := pos / cols
		c := pos % cols
		if board[r][c] == 1 {
			board[r][c] = 2
			if r+1 < rows {
				stack = append(stack, (r+1)*cols+c)
			}
			if r-1 >= 0 {
				stack = append(stack, (r-1)*cols+c)
			}
			if c+1 < cols {
				stack = append(stack, r*cols+(c+1))
			}
			if c-1 >= 0 {
				stack = append(stack, r*cols+(c-1))
			}
		}
	}
}

func solve(board [][]int64, rows int64, cols int64) {
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			onBorder := r == 0 || r == rows-1 || c == 0 || c == cols-1
			if onBorder && board[r][c] == 1 {
				flood(board, rows, cols, r, c)
			}
		}
	}
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			if board[r][c] == 2 {
				board[r][c] = 1
			} else {
				board[r][c] = 0
			}
		}
	}
}

const (
	Rows  = 300
	Cols  = 300
	Iters = 400
)

func main() {
	pristine := make([][]int64, 0, Rows)
	x := int64(5)
	for r := 0; r < Rows; r++ {
		row := make([]int64, 0, Cols)
		for c := 0; c < Cols; c++ {
			x = (x*1103515245 + 12345) % 2147483648
			row = append(row, (x/65536)%2)
		}
		pristine = append(pristine, row)
	}

	var sink int64
	for it := 0; it < Iters; it++ {
		work := make([][]int64, 0, Rows)
		for a := 0; a < Rows; a++ {
			row := make([]int64, 0, Cols)
			for b := 0; b < Cols; b++ {
				row = append(row, pristine[a][b])
			}
			work = append(work, row)
		}

		solve(work, Rows, Cols)

		var h int64
		for p := 0; p < Rows; p++ {
			for q := 0; q < Cols; q++ {
				h = (h*31 + work[p][q]) % 1000000007
			}
		}
		sink = (sink + h) % 1000000007
	}
	fmt.Println(sink)
}
