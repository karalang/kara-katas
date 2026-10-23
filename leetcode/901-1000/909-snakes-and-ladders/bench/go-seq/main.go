// LeetCode #909: Snakes and Ladders -- bench program, Go.
//
// A breadth-first search over the squares, on one 20 x 20 board, LeetCode's
// largest, built once. Each round changes one square, to a snake or ladder
// to a random square or to none, solves the board and folds the answer
// into a checksum.
package main

import "fmt"

func cell(board [][]int64, square int64) int64 {
	n := int64(len(board))
	row := (square - 1) / n
	var col int64
	if row%2 == 0 {
		col = (square - 1) % n
	} else {
		col = n - 1 - (square-1)%n
	}
	return board[n-1-row][col]
}

func snakesAndLadders(board [][]int64) int64 {
	n := int64(len(board))
	last := n * n
	moves := make([]int64, last+1)
	for i := range moves {
		moves[i] = -1
	}
	queue := []int64{1}
	moves[1] = 0
	head := 0
	for head < len(queue) {
		s := queue[head]
		head++
		if s == last {
			return moves[s]
		}
		for roll := int64(1); roll < 7; roll++ {
			if s+roll > last {
				break
			}
			here := cell(board, s+roll)
			next := here
			if here == -1 {
				next = s + roll
			}
			if moves[next] == -1 {
				moves[next] = moves[s] + 1
				queue = append(queue, next)
			}
		}
	}
	return -1
}

var seed int64 = 909

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 20
	last := n * n
	rounds := 100000
	board := make([][]int64, n)
	for i := range board {
		board[i] = make([]int64, n)
		for j := range board[i] {
			board[i][j] = -1
		}
	}
	var stuck, total, check int64
	for r := 0; r < rounds; r++ {
		s := 2 + nextRandom()%(last-2)
		row := (s - 1) / n
		var col int64
		if row%2 == 0 {
			col = (s - 1) % n
		} else {
			col = n - 1 - (s-1)%n
		}
		if nextRandom()%2 == 0 {
			board[n-1-row][col] = -1
		} else {
			board[n-1-row][col] = 1 + nextRandom()%last
		}
		got := snakesAndLadders(board)
		if got == -1 {
			stuck++
		} else {
			total += got
		}
		check = (check*31 + got + 2) % 1000000007
	}
	fmt.Printf("%d rounds on a 20 x 20 board: %d with the end out of reach, the rest summing to %d, checksum %d\n", rounds, stuck, total, check)
}
