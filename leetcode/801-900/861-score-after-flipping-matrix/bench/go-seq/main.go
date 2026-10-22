// LeetCode #861: Score After Flipping Matrix -- Go mirror of the bench
// program (the ★ arm, count each column against the first).
package main

import "fmt"

func matrixScore(grid [][]int64) int64 {
	m := int64(len(grid))
	n := len(grid[0])
	var score int64
	for j := 0; j < n; j++ {
		var ones int64
		for _, row := range grid {
			if row[j] == row[0] {
				ones++
			}
		}
		if ones < m-ones {
			ones = m - ones
		}
		score = score*2 + ones
	}
	return score
}

var seed int64 = 861

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var size int64 = 20
	var rounds int64 = 1000000
	grid := make([][]int64, size)
	for i := range grid {
		grid[i] = make([]int64, size)
		for j := range grid[i] {
			grid[i][j] = nextRandom() % 2
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		cell := nextRandom() % (size * size)
		i := cell / size
		j := cell % size
		grid[i][j] = 1 - grid[i][j]
		s := matrixScore(grid)
		grid[i][j] = 1 - grid[i][j]
		total += s
		check = (check*31 + s) % 1000000007
	}
	fmt.Printf("%d rounds on a %d by %d grid: scores sum to %d, checksum %d\n", rounds, size, size, total, check)
}
