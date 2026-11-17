// LeetCode #2245: Maximum Trailing Zeros in a Cornered Path -- the
// benchmark's Go mirror of zeros.kara: prefix sums of the twos and fives
// of each row and column, every cell tried as the corner.
package main

import "fmt"

func countFactor(v, p int64) int64 {
	count := int64(0)
	for v%p == 0 {
		v /= p
		count++
	}
	return count
}

func makeGrid(rows, cols int) [][]int64 {
	g := make([][]int64, rows)
	for i := range g {
		g[i] = make([]int64, cols)
	}
	return g
}

func maxTrailingZeros(grid [][]int64) int64 {
	m, n := len(grid), len(grid[0])
	rowTwos, rowFives := makeGrid(m, n+1), makeGrid(m, n+1)
	colTwos, colFives := makeGrid(m+1, n), makeGrid(m+1, n)
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			t := countFactor(grid[i][j], 2)
			f := countFactor(grid[i][j], 5)
			rowTwos[i][j+1] = rowTwos[i][j] + t
			rowFives[i][j+1] = rowFives[i][j] + f
			colTwos[i+1][j] = colTwos[i][j] + t
			colFives[i+1][j] = colFives[i][j] + f
		}
	}
	best := int64(0)
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			ht := [2]int64{rowTwos[i][j+1], rowTwos[i][n] - rowTwos[i][j]}
			hf := [2]int64{rowFives[i][j+1], rowFives[i][n] - rowFives[i][j]}
			vt := [2]int64{colTwos[i][j], colTwos[m][j] - colTwos[i+1][j]}
			vf := [2]int64{colFives[i][j], colFives[m][j] - colFives[i+1][j]}
			for a := 0; a < 2; a++ {
				for b := 0; b < 2; b++ {
					z := min(ht[a]+vt[b], hf[a]+vf[b])
					if z > best {
						best = z
					}
				}
			}
		}
	}
	return best
}

var seed int64 = 2245

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	check := int64(0)
	for g := 0; g < 40; g++ {
		grid := makeGrid(250, 400)
		for i := range grid {
			for j := range grid[i] {
				grid[i][j] = nextRandom()%1000 + 1
			}
		}
		check = (check*31 + maxTrailingZeros(grid) + 1) % 1000000007
	}
	fmt.Printf("40 grids of 250 x 400: checksum %d\n", check)
}
