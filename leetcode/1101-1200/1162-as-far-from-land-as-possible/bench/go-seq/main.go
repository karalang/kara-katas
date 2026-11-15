// LeetCode #1162: As Far from Land as Possible -- Go mirror of the Kāra ★
// arm: a breadth-first search from every land cell at once, over a flat
// distance array and a queue of cell indices.
package main

import "fmt"

func maxDistance(grid [][]int64) int64 {
	n := int64(len(grid))
	dist := make([]int64, n*n)
	for i := range dist {
		dist[i] = -1
	}
	queue := []int64{}
	for i := int64(0); i < n; i++ {
		for j := int64(0); j < n; j++ {
			if grid[i][j] == 1 {
				dist[i*n+j] = 0
				queue = append(queue, i*n+j)
			}
		}
	}
	if len(queue) == 0 || int64(len(queue)) == n*n {
		return -1
	}
	dirs := [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	head := 0
	far := int64(0)
	for head < len(queue) {
		cell := queue[head]
		head++
		i, j := cell/n, cell%n
		far = dist[cell]
		for _, d := range dirs {
			a, b := i+d[0], j+d[1]
			if a >= 0 && a < n && b >= 0 && b < n && dist[a*n+b] < 0 {
				dist[a*n+b] = far + 1
				queue = append(queue, a*n+b)
			}
		}
	}
	return far
}

var seed int64 = 1162

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	odds := []int64{1, 2, 5, 10, 50, 200, 500, 900}
	grids := make([][][]int64, 16)
	for k := 0; k < 16; k++ {
		o := odds[k%8]
		grids[k] = make([][]int64, 100)
		for a := 0; a < 100; a++ {
			grids[k][a] = make([]int64, 100)
			for b := 0; b < 100; b++ {
				if nextRandom()%1000 < o {
					grids[k][a][b] = 1
				}
			}
		}
	}
	var total, check int64
	for r := 0; r < 300; r++ {
		for k := 0; k < 16; k++ {
			a := nextRandom() % 100
			b := nextRandom() % 100
			grids[k][a][b] = 1 - grids[k][a][b]
			d := maxDistance(grids[k])
			total += d
			check = (check*31 + d + 1) % 1000000007
		}
	}
	fmt.Printf("300 rounds over 16 grids of 100 by 100: total %d, checksum %d\n", total, check)
}
