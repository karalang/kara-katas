// LeetCode #1219 bench, Go mirror of the Kāra ★ arm: a depth-first search
// from every cell with gold that zeroes a cell while the search goes on
// from it and puts its gold back on the way out, on 160 grids of 15 by 15,
// each holding one blob of 25 cells with gold, drawn once.
package main

import "fmt"

var seed int64 = 1219

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

var steps = [4][2]int64{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}

func collect(grid [][]int64, r, c int64) int64 {
	if r < 0 || c < 0 || r >= int64(len(grid)) || c >= int64(len(grid[0])) || grid[r][c] == 0 {
		return 0
	}
	gold := grid[r][c]
	grid[r][c] = 0
	var best int64
	for _, s := range steps {
		if v := collect(grid, r+s[0], c+s[1]); v > best {
			best = v
		}
	}
	grid[r][c] = gold
	return gold + best
}

func getMaximumGold(grid [][]int64) int64 {
	g := make([][]int64, len(grid))
	for i, row := range grid {
		g[i] = append([]int64(nil), row...)
	}
	var best int64
	for r := range g {
		for c := range g[0] {
			if g[r][c] > 0 {
				if v := collect(g, int64(r), int64(c)); v > best {
					best = v
				}
			}
		}
	}
	return best
}

func main() {
	grids := make([][][]int64, 0, 160)
	for k := 0; k < 160; k++ {
		grid := make([][]int64, 15)
		for i := range grid {
			grid[i] = make([]int64, 15)
		}
		r0 := nextRandom() % 15
		c0 := nextRandom() % 15
		grid[r0][c0] = nextRandom()%100 + 1
		cells := [][2]int64{{r0, c0}}
		for len(cells) < 25 {
			at := nextRandom() % int64(len(cells))
			s := steps[nextRandom()%4]
			r, c := cells[at][0]+s[0], cells[at][1]+s[1]
			if r >= 0 && c >= 0 && r < 15 && c < 15 && grid[r][c] == 0 {
				grid[r][c] = nextRandom()%100 + 1
				cells = append(cells, [2]int64{r, c})
			}
		}
		grids = append(grids, grid)
	}
	var check, total int64
	for _, grid := range grids {
		answer := getMaximumGold(grid)
		total += answer
		check = (check*131 + answer) % 1000000007
	}
	fmt.Printf("160 grids of 15 by 15, one blob of 25 cells with gold each: gold total %d, checksum %d\n", total, check)
}
