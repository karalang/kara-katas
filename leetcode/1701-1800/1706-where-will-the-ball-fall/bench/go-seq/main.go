// LeetCode #1706: Where Will the Ball Fall -- the bench's Go mirror: the ★
// arm on 1000 random boxes of 100 by 100, all drawn first, each answered
// 100 times.
package main

import "fmt"

// each ball followed down a row at a time
func findBall(grid [][]int32) []int32 {
	n := int64(len(grid[0]))
	answer := []int32{}
	for start := int64(0); start < n; start++ {
		c := start
		for _, row := range grid {
			next := c + int64(row[c])
			if next < 0 || next >= n || row[next] != row[c] {
				c = -1
				break
			}
			c = next
		}
		answer = append(answer, int32(c))
	}
	return answer
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1706

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, side = 1000, 100, 100
	boxes := make([][][]int32, 0, count)
	for b := 0; b < count; b++ {
		// long runs of one slope: a board turns the other way one time in 20
		grid := make([][]int32, 0, side)
		for r := 0; r < side; r++ {
			row := []int32{}
			var board int32 = 1
			for c := 0; c < side; c++ {
				if nextRandom()%20 == 0 {
					board = -board
				}
				row = append(row, board)
			}
			grid = append(grid, row)
		}
		boxes = append(boxes, grid)
	}
	var out, check int64
	for r := int64(0); r < rounds; r++ {
		for _, grid := range boxes {
			for _, a := range findBall(grid) {
				if a >= 0 {
					out++
				}
				check = (check*31 + int64(a) + 2 + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d boxes of %d by %d, %d rounds: %d balls out, checksum %d\n", count, side, side, rounds, out, check)
}
