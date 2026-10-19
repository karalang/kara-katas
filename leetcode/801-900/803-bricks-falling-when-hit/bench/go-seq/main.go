// LeetCode 803 -- Bricks Falling When Hit: the bench, mirroring
// hit_bricks.kara with the same union-find run backwards.
package main

import "fmt"

var seed int64 = 803

var dr = [4]int64{-1, 1, 0, 0}
var dc = [4]int64{0, 0, -1, 1}

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func find(parent []int64, x int64) int64 {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func union(parent, size []int64, a, b int64) {
	ra, rb := find(parent, a), find(parent, b)
	if ra == rb {
		return
	}
	if size[ra] < size[rb] {
		parent[ra] = rb
		size[rb] += size[ra]
	} else {
		parent[rb] = ra
		size[ra] += size[rb]
	}
}

// join joins the brick at (r, c) to the roof if it is in the top row,
// and to each brick next to it.
func join(r, c, rows, cols int64, left [][]int64, parent, size []int64) {
	here := r*cols + c
	if r == 0 {
		union(parent, size, here, rows*cols)
	}
	for d := 0; d < 4; d++ {
		nr, nc := r+dr[d], c+dc[d]
		if nr >= 0 && nr < rows && nc >= 0 && nc < cols && left[nr][nc] == 1 {
			union(parent, size, here, nr*cols+nc)
		}
	}
}

func hitBricks(grid [][]int64, hits [][2]int64) []int64 {
	rows, cols := int64(len(grid)), int64(len(grid[0]))
	left := make([][]int64, rows)
	for r := range grid {
		left[r] = append([]int64(nil), grid[r]...)
	}
	for _, h := range hits {
		left[h[0]][h[1]] = 0
	}
	roof := rows * cols
	parent := make([]int64, 0)
	size := make([]int64, 0)
	for i := int64(0); i < roof+1; i++ {
		parent = append(parent, i)
		size = append(size, 1)
	}
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			if left[r][c] == 1 {
				join(r, c, rows, cols, left, parent, size)
			}
		}
	}
	fallen := make([]int64, len(hits))
	for k := len(hits) - 1; k >= 0; k-- {
		r, c := hits[k][0], hits[k][1]
		if grid[r][c] == 1 {
			before := size[find(parent, roof)]
			left[r][c] = 1
			join(r, c, rows, cols, left, parent, size)
			after := size[find(parent, roof)]
			if f := after - before - 1; f > 0 {
				fallen[k] = f
			}
		}
	}
	return fallen
}

// settled is the wall with every brick that is not held up from the top
// row taken away, so that every brick starts held up.
func settled(grid [][]int64) [][]int64 {
	rows, cols := int64(len(grid)), int64(len(grid[0]))
	out := make([][]int64, rows)
	for r := range out {
		out[r] = make([]int64, cols)
	}
	stack := make([][2]int64, 0)
	for c := int64(0); c < cols; c++ {
		if grid[0][c] == 1 {
			out[0][c] = 1
			stack = append(stack, [2]int64{0, c})
		}
	}
	for len(stack) > 0 {
		top := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		r, c := top[0], top[1]
		for d := 0; d < 4; d++ {
			nr, nc := r+dr[d], c+dc[d]
			if nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 1 && out[nr][nc] == 0 {
				out[nr][nc] = 1
				stack = append(stack, [2]int64{nr, nc})
			}
		}
	}
	return out
}

func main() {
	var size int64 = 200
	walls := make([][][]int64, 0)
	allHits := make([][][2]int64, 0)
	for w := 0; w < 8; w++ {
		grid := make([][]int64, 0)
		for r := int64(0); r < size; r++ {
			row := make([]int64, 0)
			for c := int64(0); c < size; c++ {
				if nextRandom()%4 < 3 {
					row = append(row, 1)
				} else {
					row = append(row, 0)
				}
			}
			grid = append(grid, row)
		}
		walls = append(walls, settled(grid))
		cells := make([]int64, size*size)
		for j := range cells {
			cells[j] = int64(j)
		}
		for j := int64(1); j < size*size; j++ {
			t := nextRandom() % (j + 1)
			cells[j], cells[t] = cells[t], cells[j]
		}
		hits := make([][2]int64, 20000)
		for j := 0; j < 20000; j++ {
			hits[j] = [2]int64{cells[j] / size, cells[j] % size}
		}
		allHits = append(allHits, hits)
	}
	var rounds int64 = 500
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		fallen := hitBricks(walls[r%8], allHits[r%8])
		var sum int64
		for _, f := range fallen {
			sum += f
		}
		total += sum
		check = (check*131 + sum + fallen[r%20000]) % 1000000007
	}
	fmt.Printf("%d rounds of 20000 hits: %d bricks fell, checksum %d\n", rounds, total, check)
}
