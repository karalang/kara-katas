// Benchmark for #361 -- mirror of bomb_enemy.kara.
package main

import "fmt"

func maxKilledEnemies(grid [][]byte) int64 {
	rows := len(grid)
	if rows == 0 {
		return 0
	}
	cols := len(grid[0])
	var best, rowHits int64
	colHits := make([]int64, cols)
	for i := 0; i < rows; i++ {
		for j := 0; j < cols; j++ {
			if j == 0 || grid[i][j-1] == 'W' {
				rowHits = 0
				for k := j; k < cols && grid[i][k] != 'W'; k++ {
					if grid[i][k] == 'E' {
						rowHits++
					}
				}
			}
			if i == 0 || grid[i-1][j] == 'W' {
				colHits[j] = 0
				for k := i; k < rows && grid[k][j] != 'W'; k++ {
					if grid[k][j] == 'E' {
						colHits[j]++
					}
				}
			}
			if grid[i][j] == '0' && rowHits+colHits[j] > best {
				best = rowHits + colHits[j]
			}
		}
	}
	return best
}

func main() {
	var seed int64 = 361
	var total, checksum int64
	for g := 0; g < 60; g++ {
		grid := make([][]byte, 400)
		for i := range grid {
			row := make([]byte, 400)
			for j := range row {
				seed = (seed*1103515245 + 12345) % 2147483648
				r := (seed / 65536) % 6
				switch {
				case r == 0:
					row[j] = 'W'
				case r < 3:
					row[j] = 'E'
				default:
					row[j] = '0'
				}
			}
			grid[i] = row
		}
		best := maxKilledEnemies(grid)
		total += best
		checksum = (checksum*31 + best) % 1000000007
	}
	fmt.Printf("60 grids: %d enemies in total, checksum %d\n", total, checksum)
}
