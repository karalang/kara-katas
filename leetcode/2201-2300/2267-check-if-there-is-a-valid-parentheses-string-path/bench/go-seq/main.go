// LeetCode #2267: Check if There Is a Valid Parentheses String Path -- Go
// mirror of the ★ arm (path.kara): a table reach[i][j][b] of the balances
// some path to (i, j) can end with, as nested slices. Output is
// byte-identical to path.kara.
package main

import "fmt"

func hasValidPath(grid [][]byte) bool {
	m, n := len(grid), len(grid[0])
	if (m+n-1)%2 == 1 || grid[0][0] == ')' || grid[m-1][n-1] == '(' {
		return false
	}
	most := (m+n)/2 + 1
	reach := make([][][]bool, m)
	for i := range reach {
		reach[i] = make([][]bool, n)
		for j := range reach[i] {
			reach[i][j] = make([]bool, most+1)
		}
	}
	reach[0][0][1] = true
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			if i == 0 && j == 0 {
				continue
			}
			step := -1
			if grid[i][j] == '(' {
				step = 1
			}
			for b := 0; b <= most; b++ {
				from := b - step
				if from < 0 || from > most {
					continue
				}
				if (i > 0 && reach[i-1][j][from]) || (j > 0 && reach[i][j-1][from]) {
					reach[i][j][b] = true
				}
			}
		}
	}
	return reach[m-1][n-1][0]
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2267

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	found := 0
	var check int64
	for t := 0; t < 20; t++ {
		open := int64(50 + t)
		grid := make([][]byte, 100)
		for i := range grid {
			grid[i] = make([]byte, 99)
			for j := range grid[i] {
				if nextRandom()%100 < open {
					grid[i][j] = '('
				} else {
					grid[i][j] = ')'
				}
			}
		}
		grid[0][0] = '('
		grid[99][98] = ')'
		valid := hasValidPath(grid)
		v := int64(1)
		if valid {
			found++
			v = 2
		}
		check = (check*31 + v) % 1000000007
	}
	fmt.Printf("20 grids of 100 by 99: %d with a path, checksum %d\n", found, check)
}
