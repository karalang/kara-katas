// Benchmark workload for LeetCode #348 — Go mirror of tic_tac_toe.kara.
package main

import "fmt"

const (
	SIDE  = 1000
	GAMES = 100
)

type TicTacToe struct {
	n          int64
	rows, cols []int64
	diag, anti int64
}

func newTicTacToe(n int64) *TicTacToe {
	return &TicTacToe{n: n, rows: make([]int64, n), cols: make([]int64, n)}
}

func (t *TicTacToe) makeMove(row, col, player int64) int64 {
	d := int64(-1)
	if player == 1 {
		d = 1
	}
	t.rows[row] += d
	t.cols[col] += d
	if row == col {
		t.diag += d
	}
	if row+col == t.n-1 {
		t.anti += d
	}
	goal := d * t.n
	if t.rows[row] == goal || t.cols[col] == goal || t.diag == goal || t.anti == goal {
		return player
	}
	return 0
}

func main() {
	cells := int64(SIDE * SIDE)
	order := make([]int64, cells)
	for c := int64(0); c < cells; c++ {
		order[c] = c
	}
	x := int64(348)
	for k := cells - 1; k > 0; k-- {
		x = (x*1103515245 + 12345) % 2147483648
		j := x / 16 % (k + 1)
		order[k], order[j] = order[j], order[k]
	}

	sink := int64(0)
	for g := int64(0); g < GAMES; g++ {
		start := g * cells / GAMES
		game := newTicTacToe(SIDE)
		player, moves, winner := int64(1), int64(0), int64(0)
		for moves < cells && winner == 0 {
			cell := order[(start+moves)%cells]
			winner = game.makeMove(cell/SIDE, cell%SIDE, player)
			moves++
			player = 3 - player
		}
		sink = (sink*31 + moves*(winner+1)) % 1000000007
	}
	fmt.Printf("sink %d\n", sink)
}
