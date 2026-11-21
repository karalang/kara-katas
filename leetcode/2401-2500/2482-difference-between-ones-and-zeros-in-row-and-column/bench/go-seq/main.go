// LeetCode #2482: Difference Between Ones and Zeros in Row and Column --
// bench, Go mirror of diff.kara.
package main

import "fmt"

func onesMinusZeros(grid [][]int64) [][]int64 {
	m, n := len(grid), len(grid[0])
	rowOnes := make([]int64, m)
	colOnes := make([]int64, n)
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			rowOnes[i] += grid[i][j]
			colOnes[j] += grid[i][j]
		}
	}
	diff := make([][]int64, 0, m)
	for i := 0; i < m; i++ {
		row := make([]int64, 0, n)
		for j := 0; j < n; j++ {
			row = append(row, 2*rowOnes[i]+2*colOnes[j]-int64(m)-int64(n))
		}
		diff = append(diff, row)
	}
	return diff
}

var seed int64 = 2482

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grids := make([][][]int64, 20)
	for g := range grids {
		grids[g] = make([][]int64, 100)
		for i := range grids[g] {
			grids[g][i] = make([]int64, 100)
			for j := range grids[g][i] {
				grids[g][i][j] = nextRandom() % 2
			}
		}
	}
	check := int64(0)
	for p := int64(0); p < 180; p++ {
		for g := 0; g < 20; g++ {
			i, j := check%100, check/100%100
			grids[g][i][j] = 1 - grids[g][i][j]
			diff := onesMinusZeros(grids[g])
			for _, row := range diff {
				for _, v := range row {
					check = (check*31 + v + 200 + p) % 1000000007
				}
			}
		}
	}
	fmt.Printf("180 passes over 20 grids of 100 by 100: checksum %d\n", check)
}
