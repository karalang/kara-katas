// LeetCode #1301 bench: the ★ arm (a table from the bottom-right corner
// back, each square holding the most points reaching it and how many paths
// collect that many) over 20 boards of 100 by 100 with obstacles 0 to 38 in
// 100, built once; then 150 passes, each setting one square of every board to
// an obstacle or a digit from the checksum so far, answering it, and folding
// the score and the count into the checksum.
package main

import "fmt"

func pathsWithMaxScore(board []string) [2]int64 {
	n := len(board)
	grid := make([][]rune, n)
	for i, row := range board {
		grid[i] = []rune(row)
	}
	const modulus = 1000000007
	best := make([][]int64, n)
	ways := make([][]int64, n)
	for i := range best {
		best[i] = make([]int64, n)
		ways[i] = make([]int64, n)
		for j := range best[i] {
			best[i][j] = -1
		}
	}
	best[n-1][n-1] = 0
	ways[n-1][n-1] = 1
	moves := [3][2]int{{1, 0}, {0, 1}, {1, 1}}
	for i := n - 1; i >= 0; i-- {
		for j := n - 1; j >= 0; j-- {
			if grid[i][j] == 'X' || (i == n-1 && j == n-1) {
				continue
			}
			var top int64 = -1
			var count int64
			for _, m := range moves {
				a, b := i+m[0], j+m[1]
				if a < n && b < n && best[a][b] >= 0 {
					if best[a][b] > top {
						top = best[a][b]
						count = ways[a][b]
					} else if best[a][b] == top {
						count = (count + ways[a][b]) % modulus
					}
				}
			}
			if top >= 0 {
				var points int64
				if c := grid[i][j]; c >= '0' && c <= '9' {
					points = int64(c - '0')
				}
				best[i][j] = top + points
				ways[i][j] = count
			}
		}
	}
	if best[0][0] < 0 {
		return [2]int64{0, 0}
	}
	return [2]int64{best[0][0], ways[0][0]}
}

var seed int64 = 1301

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	boards := [][]string{}
	for t := int64(0); t < 20; t++ {
		wall := 2 * t
		board := []string{}
		for i := 0; i < 100; i++ {
			row := []rune{}
			for j := 0; j < 100; j++ {
				if i == 0 && j == 0 {
					row = append(row, 'E')
				} else if i == 99 && j == 99 {
					row = append(row, 'S')
				} else if nextRandom()%100 < wall {
					row = append(row, 'X')
				} else {
					row = append(row, rune('0'+nextRandom()%9+1))
				}
			}
			board = append(board, string(row))
		}
		boards = append(boards, board)
	}
	var check int64
	for p := int64(0); p < 150; p++ {
		for _, board := range boards {
			at := 1 + check%9998
			i, j := at/100, at%100
			cells := []rune(board[i])
			if check%7 == 0 {
				cells[j] = 'X'
			} else {
				cells[j] = rune('0' + check%9 + 1)
			}
			board[i] = string(cells)
			got := pathsWithMaxScore(board)
			check = (check*31 + got[0] + p) % 1000000007
			check = (check*31 + got[1]) % 1000000007
		}
	}
	fmt.Printf("150 passes over 20 boards of 100 by 100: checksum %d\n", check)
}
