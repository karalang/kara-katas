// LeetCode #1277 bench, in Go: the ★ arm (dynamic programming over the
// sides of the largest squares) on 40 random 300-by-300 matrices, half,
// four fifths, nineteen twentieths and 99 in 100 ones, drawn once; 50
// rounds, every count folded into a checksum.
package main

import "fmt"

func countSquares(matrix [][]int64) int64 {
	m, n := len(matrix), len(matrix[0])
	side := make([][]int64, m)
	for i := range side {
		side[i] = make([]int64, n)
	}
	var total int64
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			if matrix[i][j] == 1 {
				if i == 0 || j == 0 {
					side[i][j] = 1
				} else {
					side[i][j] = min(side[i-1][j], side[i][j-1], side[i-1][j-1]) + 1
				}
				total += side[i][j]
			}
		}
	}
	return total
}

var seed int64 = 1277

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	percents := []int64{50, 80, 95, 99}
	matrices := make([][][]int64, 0, 40)
	for k := 0; k < 40; k++ {
		matrix := make([][]int64, 0, 300)
		for i := 0; i < 300; i++ {
			row := make([]int64, 300)
			for j := range row {
				if nextRandom()%100 < percents[k%4] {
					row[j] = 1
				}
			}
			matrix = append(matrix, row)
		}
		matrices = append(matrices, matrix)
	}
	var check int64
	for round := int64(0); round < 50; round++ {
		for _, matrix := range matrices {
			check = (check*131 + countSquares(matrix) + round) % 1000000007
		}
	}
	fmt.Printf("50 rounds of 40 matrices of 300 by 300: checksum %d\n", check)
}
