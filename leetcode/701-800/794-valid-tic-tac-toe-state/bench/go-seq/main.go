// LeetCode 794 — Valid Tic-Tac-Toe State: the bench, in Go. Mirrors
// valid_tic_tac_toe.kara: count the marks and check the lines.
package main

import "fmt"

var lines = [8][3]int{{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}}

func wins(cells []byte, mark byte) bool {
	for _, l := range lines {
		if cells[l[0]] == mark && cells[l[1]] == mark && cells[l[2]] == mark {
			return true
		}
	}
	return false
}

func validTicTacToe(board []string) bool {
	cells := make([]byte, 0, 9)
	for _, row := range board {
		cells = append(cells, row...)
	}
	x, o := 0, 0
	for _, c := range cells {
		if c == 'X' {
			x++
		} else if c == 'O' {
			o++
		}
	}
	if x != o && x != o+1 {
		return false
	}
	if wins(cells, 'X') && x != o+1 {
		return false
	}
	if wins(cells, 'O') && x != o {
		return false
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomBoard(seed *int64) []string {
	cells := []byte("         ")
	if nextRandom(seed)%2 == 0 {
		marks := []byte{' ', 'X', 'O'}
		for i := range cells {
			cells[i] = marks[nextRandom(seed)%3]
		}
	} else {
		moves := nextRandom(seed) % 10
		mover := byte('X')
		for m := int64(0); m < moves; m++ {
			var empty []int
			for i := 0; i < 9; i++ {
				if cells[i] == ' ' {
					empty = append(empty, i)
				}
			}
			cells[empty[nextRandom(seed)%int64(len(empty))]] = mover
			if mover == 'X' {
				mover = 'O'
			} else {
				mover = 'X'
			}
		}
	}
	return []string{string(cells[0:3]), string(cells[3:6]), string(cells[6:9])}
}

func main() {
	seed := int64(794)
	boards := make([][]string, 4096)
	for k := range boards {
		boards[k] = randomBoard(&seed)
	}
	rounds := 6000000
	var valid, check int64
	for r := 0; r < rounds; r++ {
		if validTicTacToe(boards[r%4096]) {
			valid++
			check = (check*131 + int64(r%4096)) % 1000000007
		}
	}
	fmt.Printf("%d boards: %d valid, checksum %d\n", rounds, valid, check)
}
