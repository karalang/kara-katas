// LeetCode #867: Transpose Matrix -- Go mirror of the bench program (the ★
// arm, one column at a time), with 64-bit entries as in the Kāra program.
package main

import "fmt"

func transpose(matrix [][]int64) [][]int64 {
	rows := len(matrix)
	cols := len(matrix[0])
	var out [][]int64
	for c := 0; c < cols; c++ {
		var row []int64
		for r := 0; r < rows; r++ {
			row = append(row, matrix[r][c])
		}
		out = append(out, row)
	}
	return out
}

var seed int64 = 867

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomValue() int64 {
	hi := nextRandom()
	lo := nextRandom()
	return (hi*32768+lo)%2000000001 - 1000000000
}

func main() {
	var m [][]int64
	for r := 0; r < 1000; r++ {
		var row []int64
		for c := 0; c < 100; c++ {
			row = append(row, randomValue())
		}
		m = append(m, row)
	}
	rounds := 6000
	var check int64
	for round := 0; round < rounds; round++ {
		m = transpose(m)
		r := round * 7 % len(m)
		c := round * 13 % len(m[0])
		check = (check*31 + m[r][c]%1000000007 + 1000000007) % 1000000007
	}
	for _, row := range m {
		for _, v := range row {
			check = (check*31 + v%1000000007 + 1000000007) % 1000000007
		}
	}
	fmt.Printf("%d transposes of a 1000 x 100 matrix: %d x %d, checksum %d\n", rounds, len(m), len(m[0]), check)
}
