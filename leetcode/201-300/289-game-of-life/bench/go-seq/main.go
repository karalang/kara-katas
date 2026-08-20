// Benchmark twin for LeetCode #289 — same algorithm as gameoflife.kara.
//
// Two-bit in-place encoding: bit 0 old generation, bit 1 new.
package main

import "fmt"

const rows, cols, gens = 256, 256, 60

var board [rows][cols]int64

func nextRand(s int64) int64 { return (s*1103515245 + 12345) & 2147483647 }

func liveNeighbours(r, c int) int64 {
	var n int64
	for dr := -1; dr <= 1; dr++ {
		for dc := -1; dc <= 1; dc++ {
			if dr == 0 && dc == 0 {
				continue
			}
			rr, cc := r+dr, c+dc
			if rr >= 0 && rr < rows && cc >= 0 && cc < cols {
				n += board[rr][cc] & 1
			}
		}
	}
	return n
}

func step() {
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			n := liveNeighbours(r, c)
			alive := board[r][c]&1 == 1
			var lives bool
			if alive {
				lives = n == 2 || n == 3
			} else {
				lives = n == 3
			}
			if lives {
				board[r][c] |= 2
			}
		}
	}
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			board[r][c] >>= 1
		}
	}
}

func main() {
	seed := int64(20260820)
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			seed = nextRand(seed)
			if (seed/65536)%100 < 35 {
				board[r][c] = 1
			} else {
				board[r][c] = 0
			}
		}
	}
	for g := 0; g < gens; g++ {
		step()
	}

	var pop, hash int64
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if board[r][c] == 1 {
				pop++
				hash = (hash*31 + int64(r)*cols + int64(c)) % 1000000007
			}
		}
	}
	fmt.Printf("pop %d hash %d\n", pop, hash)
}
