// Benchmark for #542: Go mirror of the ★ arm (breadth-first search from
// every 0 at once); see ../update_matrix.kara. The queue is a slice with
// a moving head.
package main

import "fmt"

func updateMatrix(mat [][]int64) [][]int64 {
	m, n := len(mat), len(mat[0])
	dist := make([][]int64, m)
	queue := [][2]int{}
	for r := 0; r < m; r++ {
		dist[r] = make([]int64, n)
		for c := 0; c < n; c++ {
			if mat[r][c] == 0 {
				queue = append(queue, [2]int{r, c})
			} else {
				dist[r][c] = -1
			}
		}
	}
	steps := [4][2]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for head := 0; head < len(queue); head++ {
		r, c := queue[head][0], queue[head][1]
		for _, s := range steps {
			nr, nc := r+s[0], c+s[1]
			if nr >= 0 && nr < m && nc >= 0 && nc < n && dist[nr][nc] < 0 {
				dist[nr][nc] = dist[r][c] + 1
				queue = append(queue, [2]int{nr, nc})
			}
		}
	}
	return dist
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 20 random 100 by 100 grids (the problem's 10,000 cells), from half
	// ones to 88 in a hundred, built once. Then 50 times over every grid
	// is answered; one row of the answer, picked by the round and the
	// grid, is summed, and one cell goes into the checksum.
	grids := 20
	seed := int64(542)
	all := make([][][]int64, grids)
	for g := 0; g < grids; g++ {
		ones := int64(50 + 2*g)
		all[g] = make([][]int64, 100)
		for i := range all[g] {
			all[g][i] = make([]int64, 100)
			for j := range all[g][i] {
				if nextRandom(&seed)%100 < ones {
					all[g][i][j] = 1
				}
			}
		}
	}
	var total, checksum int64
	for r := 0; r < 50; r++ {
		for t := 0; t < grids; t++ {
			answer := updateMatrix(all[t])
			for _, d := range answer[(r*7+t*13)%100] {
				total += d
			}
			cell := answer[(r*11+t*3)%100][(r*5+t*17)%100]
			checksum = (checksum*31 + cell) % 1000000007
		}
	}
	fmt.Printf("%d grids, 50 times each: row sum %d, checksum %d\n", grids, total, checksum)
}
