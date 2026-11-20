// LeetCode #1284 bench, in Go: the ★ arm (breadth-first search over bit
// masks) on every matrix of every shape, 1 by 1 to 3 by 3, 3000 rounds,
// every answer folded into a checksum.
package main

import "fmt"

func minFlips(mat [][]int64) int64 {
	rows, cols := int64(len(mat)), int64(len(mat[0]))
	cells := rows * cols
	var start int64
	flip := make([]int64, 0)
	for i := int64(0); i < rows; i++ {
		for j := int64(0); j < cols; j++ {
			if mat[i][j] == 1 {
				start |= 1 << (i*cols + j)
			}
			mask := int64(1) << (i*cols + j)
			if i > 0 {
				mask |= 1 << ((i-1)*cols + j)
			}
			if i+1 < rows {
				mask |= 1 << ((i+1)*cols + j)
			}
			if j > 0 {
				mask |= 1 << (i*cols + j - 1)
			}
			if j+1 < cols {
				mask |= 1 << (i*cols + j + 1)
			}
			flip = append(flip, mask)
		}
	}
	dist := make([]int64, 1<<cells)
	for s := range dist {
		dist[s] = -1
	}
	dist[start] = 0
	queue := []int64{start}
	for len(queue) > 0 {
		state := queue[0]
		queue = queue[1:]
		if state == 0 {
			return dist[state]
		}
		for _, mask := range flip {
			next := state ^ mask
			if dist[next] < 0 {
				dist[next] = dist[state] + 1
				queue = append(queue, next)
			}
		}
	}
	return -1
}

func matrix(rows, cols, bits int64) [][]int64 {
	mat := make([][]int64, 0)
	for i := int64(0); i < rows; i++ {
		row := make([]int64, 0)
		for j := int64(0); j < cols; j++ {
			row = append(row, (bits>>(i*cols+j))&1)
		}
		mat = append(mat, row)
	}
	return mat
}

func main() {
	var check int64
	for round := int64(0); round < 3000; round++ {
		for rows := int64(1); rows < 4; rows++ {
			for cols := int64(1); cols < 4; cols++ {
				for bits := int64(0); bits < 1<<(rows*cols); bits++ {
					check = (check*131 + minFlips(matrix(rows, cols, bits)) + round + 2) % 1000000007
				}
			}
		}
	}
	fmt.Printf("3000 rounds of every matrix: checksum %d\n", check)
}
