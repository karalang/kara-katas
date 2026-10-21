// Benchmark for #827: Making A Large Island -- the ★ arm (label, then try each 0).
//
// Mirrors largest_island.kara: a breadth-first search on a queue gives
// every island a label and records its size, and each 0 adds 1 to the
// sizes of the distinct labels around it.
package main

import "fmt"

type cell struct{ r, c int64 }

func largestIsland(grid [][]int64) int64 {
	n := int64(len(grid))
	label := make([][]int64, n)
	for r := range label {
		label[r] = make([]int64, n)
	}
	var size []int64
	dr := [4]int64{-1, 1, 0, 0}
	dc := [4]int64{0, 0, -1, 1}
	var queue []cell
	for r := int64(0); r < n; r++ {
		for c := int64(0); c < n; c++ {
			if grid[r][c] == 1 && label[r][c] == 0 {
				id := int64(len(size)) + 1
				label[r][c] = id
				queue = append(queue[:0], cell{r, c})
				count := int64(0)
				for head := 0; head < len(queue); head++ {
					cur := queue[head]
					count++
					for k := 0; k < 4; k++ {
						nr, nc := cur.r+dr[k], cur.c+dc[k]
						if nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 1 && label[nr][nc] == 0 {
							label[nr][nc] = id
							queue = append(queue, cell{nr, nc})
						}
					}
				}
				size = append(size, count)
			}
		}
	}
	var best int64
	for _, s := range size {
		if s > best {
			best = s
		}
	}
	for r := int64(0); r < n; r++ {
		for c := int64(0); c < n; c++ {
			if grid[r][c] == 0 {
				var seen []int64
				made := int64(1)
				for k := 0; k < 4; k++ {
					nr, nc := r+dr[k], c+dc[k]
					if nr >= 0 && nr < n && nc >= 0 && nc < n {
						id := label[nr][nc]
						found := false
						for _, s := range seen {
							if s == id {
								found = true
							}
						}
						if id > 0 && !found {
							seen = append(seen, id)
							made += size[id-1]
						}
					}
				}
				if made > best {
					best = made
				}
			}
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 16
	rounds := 200
	n := 500
	seed := int64(827)
	grids := make([][][]int64, 0, count)
	for g := 0; g < count; g++ {
		grid := make([][]int64, n)
		for r := range grid {
			grid[r] = make([]int64, n)
			for c := range grid[r] {
				if nextRandom(&seed)%100 < 55 {
					grid[r][c] = 1
				}
			}
		}
		grids = append(grids, grid)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		r := largestIsland(grids[round%count])
		total += r
		checksum = (checksum*131 + r) % 1000000007
	}
	fmt.Printf("%d rounds of %d grids: total %d, checksum %d\n", rounds, count, total, checksum)
}
