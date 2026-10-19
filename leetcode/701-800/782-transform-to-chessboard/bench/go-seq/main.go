// Benchmark for #782: Transform to Chessboard -- mirror of the ★ arm (the
// corner rule and two counts), with the same workload as the Kāra program.
package main

import "fmt"

func movesToChessboard(board [][]int64) int64 {
	n := int64(len(board))
	for r := int64(0); r < n; r++ {
		for c := int64(0); c < n; c++ {
			if board[0][0]^board[r][0]^board[0][c]^board[r][c] == 1 {
				return -1
			}
		}
	}
	var rowOnes, colOnes, rowOff, colOff int64
	for i := int64(0); i < n; i++ {
		rowOnes += board[0][i]
		colOnes += board[i][0]
		if board[i][0] == i%2 {
			rowOff++
		}
		if board[0][i] == i%2 {
			colOff++
		}
	}
	if rowOnes != n/2 && rowOnes != (n+1)/2 {
		return -1
	}
	if colOnes != n/2 && colOnes != (n+1)/2 {
		return -1
	}
	if n%2 == 1 {
		if rowOff%2 == 1 {
			rowOff = n - rowOff
		}
		if colOff%2 == 1 {
			colOff = n - colOff
		}
	} else {
		if n-rowOff < rowOff {
			rowOff = n - rowOff
		}
		if n-colOff < colOff {
			colOff = n - colOff
		}
	}
	return (rowOff + colOff) / 2
}

var seed int64 = 782

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n = 64, 30
	boards := make([][][]int64, count)
	for g := 0; g < count; g++ {
		rowOf := make([]int64, n)
		colOf := make([]int64, n)
		for i := range rowOf {
			rowOf[i] = int64(i)
			colOf[i] = int64(i)
		}
		for i := int64(n - 1); i > 0; i-- {
			j := nextRandom() % (i + 1)
			rowOf[i], rowOf[j] = rowOf[j], rowOf[i]
			j = nextRandom() % (i + 1)
			colOf[i], colOf[j] = colOf[j], colOf[i]
		}
		board := make([][]int64, n)
		for r := 0; r < n; r++ {
			board[r] = make([]int64, n)
			for c := 0; c < n; c++ {
				board[r][c] = (rowOf[r] + colOf[c]) % 2
			}
		}
		if g%4 == 1 {
			r := nextRandom() % n
			c := nextRandom() % n
			board[r][c] = 1 - board[r][c]
		} else if g%4 == 3 {
			for c := 0; c < n; c++ {
				board[0][c] = nextRandom() % 2
			}
			for r := 1; r < n; r++ {
				flip := nextRandom() % 2
				for c := 0; c < n; c++ {
					board[r][c] = board[0][c] ^ flip
				}
			}
		}
		boards[g] = board
	}
	var solvable, checksum int64
	for round := int64(0); round < 2000000; round++ {
		g := (round * 7) % count
		answer := movesToChessboard(boards[g])
		if answer >= 0 {
			solvable++
		}
		checksum = (checksum*31 + answer + 2 + g) % 1000000007
	}
	fmt.Printf("2000000 rounds of 30 x 30 boards: %d solvable, checksum %d\n", solvable, checksum)
}
