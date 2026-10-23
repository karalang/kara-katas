// LeetCode #892 bench: Go mirror of surface_area.kara (the ★ arm, six
// faces a cube, less the shared ones) on the same 400 grids and 80
// passes.
package main

import "fmt"

func surfaceArea(grid [][]int64) int64 {
	n := len(grid)
	var area int64
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			v := grid[i][j]
			if v > 0 {
				area += 4*v + 2
			}
			if i+1 < n {
				area -= 2 * min(v, grid[i+1][j])
			}
			if j+1 < n {
				area -= 2 * min(v, grid[i][j+1])
			}
		}
	}
	return area
}

var seed int64 = 892

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grids := make([][][]int64, 0, 400)
	for g := 0; g < 400; g++ {
		grid := make([][]int64, 0, 50)
		for i := 0; i < 50; i++ {
			row := make([]int64, 0, 50)
			for j := 0; j < 50; j++ {
				row = append(row, nextRandom()%51)
			}
			grid = append(grid, row)
		}
		grids = append(grids, grid)
	}
	var total, check int64
	for pass := 0; pass < 80; pass++ {
		for g := range grids {
			i := (pass*7 + g) % 50
			j := (pass*13 + g*3) % 50
			grids[g][i][j]++
			got := surfaceArea(grids[g])
			total += got
			check = (check*131 + got) % 1000000007
		}
	}
	fmt.Printf("32000 measurements of 400 grids of 50 by 50: surface area %d, checksum %d\n", total, check)
}
