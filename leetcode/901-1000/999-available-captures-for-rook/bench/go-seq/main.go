// Benchmark: LeetCode #999 Available Captures for Rook -- the ★ arm, a
// walk from the rook each way, on random 8 by 8 boards. Mirrors
// num_rook_captures.kara, .c, .rs and .py. The board is LeetCode's Go
// shape, [][]byte.
package main

import "fmt"

func numRookCaptures(board [][]byte) int64 {
	rr, rc := 0, 0
	for r := 0; r < 8; r++ {
		for c := 0; c < 8; c++ {
			if board[r][c] == 'R' {
				rr, rc = r, c
			}
		}
	}
	var captures int64
	for _, d := range [4][2]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}} {
		r, c := rr+d[0], rc+d[1]
		for r >= 0 && r < 8 && c >= 0 && c < 8 {
			if board[r][c] == 'p' {
				captures++
				break
			}
			if board[r][c] == 'B' {
				break
			}
			r += d[0]
			c += d[1]
		}
	}
	return captures
}

var seed int64 = 999

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds = 500000
	// 20 boards, the rook on a random square and each other square a pawn
	// 4 times in 16 and a bishop 2 times in 16
	boards := make([][][]byte, 20)
	for b := range boards {
		rook := nextRandom() % 64
		board := make([][]byte, 8)
		for r := 0; r < 8; r++ {
			row := make([]byte, 8)
			for c := 0; c < 8; c++ {
				x := nextRandom() % 16
				switch {
				case int64(r*8+c) == rook:
					row[c] = 'R'
				case x < 4:
					row[c] = 'p'
				case x < 6:
					row[c] = 'B'
				default:
					row[c] = '.'
				}
			}
			board[r] = row
		}
		boards[b] = board
	}
	var captures, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			k := (r + i) % 20
			got := numRookCaptures(boards[k])
			captures += got
			check = (check*31 + got + 1) % 1000000007
			// a pawn put on or taken off one square, so no board stays put
			s := (r*13 + i*5) % 64
			cell := &boards[k][s/8][s%8]
			if *cell == '.' {
				*cell = 'p'
			} else if *cell == 'p' {
				*cell = '.'
			}
		}
	}
	fmt.Printf("%d rounds over 20 boards: %d captures, checksum %d\n", rounds, captures, check)
}
