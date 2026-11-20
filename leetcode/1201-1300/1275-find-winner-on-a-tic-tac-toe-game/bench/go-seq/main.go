// LeetCode #1275 bench, in Go: the ★ arm (line sums) asked about every
// position of every game of tic-tac-toe, 549,945 of them, each game carried
// on while the answer is "Pending"; 40 rounds, every answer folded into a
// checksum.
package main

import "fmt"

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func tictactoe(moves [][]int64) string {
	var rows, cols [3]int64
	var diagonal, anti int64
	turn := int64(1)
	for _, m := range moves {
		r, c := m[0], m[1]
		rows[r] += turn
		cols[c] += turn
		if r == c {
			diagonal += turn
		}
		if r+c == 2 {
			anti += turn
		}
		if abs(rows[r]) == 3 || abs(cols[c]) == 3 || abs(diagonal) == 3 || abs(anti) == 3 {
			if turn == 1 {
				return "A"
			}
			return "B"
		}
		turn = -turn
	}
	if len(moves) == 9 {
		return "Draw"
	}
	return "Pending"
}

func walk(moves *[][]int64, check *int64) {
	for square := int64(0); square < 9; square++ {
		r, c := square/3, square%3
		taken := false
		for _, m := range *moves {
			if m[0] == r && m[1] == c {
				taken = true
				break
			}
		}
		if taken {
			continue
		}
		*moves = append(*moves, []int64{r, c})
		answer := tictactoe(*moves)
		var k int64
		switch answer {
		case "A":
			k = 0
		case "B":
			k = 1
		case "Draw":
			k = 2
		default:
			k = 3
		}
		*check = (*check*7 + k) % 1000000007
		if k == 3 {
			walk(moves, check)
		}
		*moves = (*moves)[:len(*moves)-1]
	}
}

func main() {
	var check int64
	for round := int64(0); round < 40; round++ {
		moves := [][]int64{}
		walk(&moves, &check)
		check = (check*131 + round) % 1000000007
	}
	fmt.Printf("40 rounds of every game: checksum %d\n", check)
}
