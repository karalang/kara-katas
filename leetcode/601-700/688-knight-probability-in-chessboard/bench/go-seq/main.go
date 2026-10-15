// LeetCode #688: Knight Probability in Chessboard -- the chances, forward.
// Bench.
//
// 60 queries, boards of 15 to 25 squares a side and 50 to 100 moves from
// a random start, are drawn once; then 50 rounds answer every query.

package main

import "fmt"

var dr = [8]int64{2, 1, -1, -2, -2, -1, 1, 2}
var dc = [8]int64{1, 2, 2, 1, -1, -2, -2, -1}

func knightProbability(n, k, row, column int64) float64 {
	board := make([]float64, n*n)
	board[row*n+column] = 1.0
	for s := int64(0); s < k; s++ {
		next := make([]float64, n*n)
		for r := int64(0); r < n; r++ {
			for c := int64(0); c < n; c++ {
				p := board[r*n+c]
				if p > 0.0 {
					for m := 0; m < 8; m++ {
						r2 := r + dr[m]
						c2 := c + dc[m]
						if r2 >= 0 && r2 < n && c2 >= 0 && c2 < n {
							next[r2*n+c2] += p / 8.0
						}
					}
				}
			}
		}
		board = next
	}
	total := 0.0
	for _, p := range board {
		total += p
	}
	return total
}

var seed int64 = 688

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 60, 50
	var qs [count][4]int64
	for q := 0; q < count; q++ {
		n := 15 + nextRandom()%11
		k := 50 + nextRandom()%51
		row := nextRandom() % n
		column := nextRandom() % n
		qs[q] = [4]int64{n, k, row, column}
	}
	sum := 0.0
	for r := 0; r < rounds; r++ {
		for q := 0; q < count; q++ {
			sum += knightProbability(qs[q][0], qs[q][1], qs[q][2], qs[q][3])
		}
	}
	fmt.Printf("%d queries answered, sum %.6f\n", count*rounds, sum)
}
