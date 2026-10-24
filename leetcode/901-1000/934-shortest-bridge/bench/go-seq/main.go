// LeetCode #934: Shortest Bridge -- bench: mark one island, then search
// outward. Mirrors shortest_bridge.kara, .c, .rs and .py.

package main

import "fmt"

var dr = [4]int64{-1, 1, 0, 0}
var dc = [4]int64{0, 0, -1, 1}

func shortestBridge(grid [][]int64) int64 {
	n := int64(len(grid))
	dist := make([]int64, n*n)
	for i := range dist {
		dist[i] = -1
	}
	var start int64
	for grid[start/n][start%n] == 0 {
		start++
	}
	stack := []int64{start}
	frontier := []int64{}
	dist[start] = 0
	for len(stack) > 0 {
		cell := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		frontier = append(frontier, cell)
		for d := 0; d < 4; d++ {
			r := cell/n + dr[d]
			c := cell%n + dc[d]
			if r >= 0 && r < n && c >= 0 && c < n && grid[r][c] == 1 && dist[r*n+c] < 0 {
				dist[r*n+c] = 0
				stack = append(stack, r*n+c)
			}
		}
	}
	head := 0
	for head < len(frontier) {
		cell := frontier[head]
		head++
		for d := 0; d < 4; d++ {
			r := cell/n + dr[d]
			c := cell%n + dc[d]
			if r >= 0 && r < n && c >= 0 && c < n && dist[r*n+c] < 0 {
				if grid[r][c] == 1 {
					return dist[cell]
				}
				dist[r*n+c] = dist[cell] + 1
				frontier = append(frontier, r*n+c)
			}
		}
	}
	return -1
}

var seed int64 = 934

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func beside(grid [][]int64, r, c, mark int64) bool {
	n := int64(len(grid))
	return (r > 0 && grid[r-1][c] == mark) || (r+1 < n && grid[r+1][c] == mark) ||
		(c > 0 && grid[r][c-1] == mark) || (c+1 < n && grid[r][c+1] == mark)
}

func grow(grid [][]int64, cells []int64, size, mark, avoid int64) []int64 {
	n := int64(len(grid))
	var tries int64
	for int64(len(cells)) < size && tries < 4*size {
		tries++
		cell := cells[nextRandom()%int64(len(cells))]
		d := nextRandom() % 4
		r := cell/n + dr[d]
		c := cell%n + dc[d]
		if r >= 0 && r < n && c >= 0 && c < n && grid[r][c] == 0 && !beside(grid, r, c, avoid) {
			grid[r][c] = mark
			cells = append(cells, r*n+c)
		}
	}
	return cells
}

func randomIslands(n, sizeA, sizeB int64) [][]int64 {
	for {
		grid := make([][]int64, n)
		for r := range grid {
			grid[r] = make([]int64, n)
		}
		a := nextRandom() % (n * n)
		grid[a/n][a%n] = 2
		grow(grid, []int64{a}, sizeA, 2, -1)
		var b int64 = -1
		for k := 0; k < 100; k++ {
			x := nextRandom() % (n * n)
			if b < 0 && grid[x/n][x%n] == 0 && !beside(grid, x/n, x%n, 2) {
				b = x
			}
		}
		if b >= 0 {
			grid[b/n][b%n] = 3
			grow(grid, []int64{b}, sizeB, 3, 2)
			for _, row := range grid {
				for c := range row {
					if row[c] > 0 {
						row[c] = 1
					}
				}
			}
			return grid
		}
	}
}

func main() {
	var rounds int64 = 50
	var count int64 = 100
	var n int64 = 100
	// count n x n grids, each with two islands of up to 2500 cells grown
	// at random, built once
	grids := make([][][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		sizeA := 1 + nextRandom()%2500
		sizeB := 1 + nextRandom()%2500
		grids = append(grids, randomIslands(n, sizeA, sizeB))
	}
	var total int64
	var check int64
	for r := int64(0); r < rounds; r++ {
		// each round visits every grid, starting from a different one
		for i := int64(0); i < count; i++ {
			a := shortestBridge(grids[(r+i)%count])
			total += a
			check = (check*1000003 + a) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d grids of %d x %d: answers summing to %d, checksum %d\n", rounds, count, n, n, total, check)
}
