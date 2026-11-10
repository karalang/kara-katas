// LeetCode #2056: Number of Valid Move Combinations On Chessboard -- Go
// mirror of the ★ arm's benchmark (moves.kara): the same 200 boards of 4
// pieces, the same moves and backtracking, each new move walked against the
// moves already chosen.
package main

import "fmt"

type move struct{ dr, dc, steps int64 }

type square struct{ r, c int64 }

var seed int64 = 2056

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func movesOf(kind string, r, c int64) []move {
	var dirs [][2]int64
	if kind != "bishop" {
		dirs = append(dirs, [2]int64{1, 0}, [2]int64{-1, 0}, [2]int64{0, 1}, [2]int64{0, -1})
	}
	if kind != "rook" {
		dirs = append(dirs, [2]int64{1, 1}, [2]int64{1, -1}, [2]int64{-1, 1}, [2]int64{-1, -1})
	}
	moves := []move{{0, 0, 0}}
	for _, d := range dirs {
		for steps := int64(1); r+d[0]*steps >= 1 && r+d[0]*steps <= 8 && c+d[1]*steps >= 1 && c+d[1]*steps <= 8; steps++ {
			moves = append(moves, move{d[0], d[1], steps})
		}
	}
	return moves
}

func collide(a square, ma move, b square, mb move) bool {
	for t := int64(1); t <= max(ma.steps, mb.steps); t++ {
		ta, tb := min(t, ma.steps), min(t, mb.steps)
		if a.r+ma.dr*ta == b.r+mb.dr*tb && a.c+ma.dc*ta == b.c+mb.dc*tb {
			return true
		}
	}
	return false
}

func countFrom(i int, at []square, options [][]move, chosen []move) int64 {
	if i == len(at) {
		return 1
	}
	var total int64
	for _, m := range options[i] {
		ok := true
		for j := 0; j < i && ok; j++ {
			if collide(at[j], chosen[j], at[i], m) {
				ok = false
			}
		}
		if ok {
			total += countFrom(i+1, at, options, append(chosen, m))
		}
	}
	return total
}

func countCombinations(pieces []string, positions []square) int64 {
	options := make([][]move, len(pieces))
	for i := range pieces {
		options[i] = movesOf(pieces[i], positions[i].r, positions[i].c)
	}
	return countFrom(0, positions, options, make([]move, 0, len(pieces)))
}

func main() {
	kinds := []string{"rook", "queen", "bishop"}
	var total, check int64
	for b := 0; b < 200; b++ {
		var pieces []string
		var positions []square
		for len(positions) < 4 {
			r := nextRandom()%8 + 1
			c := nextRandom()%8 + 1
			kind := kinds[nextRandom()%3]
			seen := false
			for _, p := range positions {
				if p.r == r && p.c == c {
					seen = true
				}
			}
			if !seen {
				pieces = append(pieces, kind)
				positions = append(positions, square{r, c})
			}
		}
		count := countCombinations(pieces, positions)
		total += count
		check = (check*31 + count) % 1000000007
	}
	fmt.Printf("200 boards: sum %d, checksum %d\n", total, check)
}
