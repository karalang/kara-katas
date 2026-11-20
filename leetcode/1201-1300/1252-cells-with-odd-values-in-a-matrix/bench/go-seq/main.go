// LeetCode #1252 bench, in Go: the ★ arm (the matrix itself, every cell of
// each place's row and column raised by one, then the odd cells counted)
// on 1000 random lists of 100 places in a 50 by 50 matrix built once,
// each asked 40 times; every count folded into a checksum.
package main

import "fmt"

var seed int64 = 1252

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func oddCells(m, n int, indices [][2]int) int64 {
	matrix := make([][]int64, m)
	for i := range matrix {
		matrix[i] = make([]int64, n)
	}
	for _, place := range indices {
		r, c := place[0], place[1]
		for j := 0; j < n; j++ {
			matrix[r][j]++
		}
		for i := 0; i < m; i++ {
			matrix[i][c]++
		}
	}
	var odd int64
	for _, row := range matrix {
		for _, v := range row {
			if v%2 == 1 {
				odd++
			}
		}
	}
	return odd
}

func main() {
	cases := make([][][2]int, 0, 1000)
	for t := 0; t < 1000; t++ {
		indices := make([][2]int, 0, 100)
		for p := 0; p < 100; p++ {
			r := int(nextRandom() % 50)
			c := int(nextRandom() % 50)
			indices = append(indices, [2]int{r, c})
		}
		cases = append(cases, indices)
	}
	var check int64
	for r := 0; r < 40; r++ {
		for _, indices := range cases {
			check = (check*131 + oddCells(50, 50, indices)) % 1000000007
		}
	}
	fmt.Printf("40 rounds of 1000 lists of 100 places in 50 by 50: checksum %d\n", check)
}
