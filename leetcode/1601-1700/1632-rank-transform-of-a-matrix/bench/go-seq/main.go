// LeetCode #1632: Rank Transform of a Matrix -- the bench's Go mirror: the
// ★ arm on 12 random 300 x 300 matrices of values 0 to 9999, all drawn
// first.
package main

import (
	"fmt"
	"sort"
)

type cell struct {
	value int32
	r, c  int64
}

func find(parent []int64, x int64) int64 {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func matrixRankTransform(matrix [][]int32) [][]int32 {
	rows, cols := int64(len(matrix)), int64(len(matrix[0]))
	cells := make([]cell, 0, rows*cols)
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			cells = append(cells, cell{matrix[r][c], r, c})
		}
	}
	sort.Slice(cells, func(i, j int) bool {
		a, b := cells[i], cells[j]
		if a.value != b.value {
			return a.value < b.value
		}
		if a.r != b.r {
			return a.r < b.r
		}
		return a.c < b.c
	})
	rowMax := make([]int32, rows)
	colMax := make([]int32, cols)
	answer := make([][]int32, rows)
	for r := range answer {
		answer[r] = make([]int32, cols)
	}
	parent := make([]int64, rows*cols)
	for i := range parent {
		parent[i] = int64(i)
	}
	start := 0
	for start < len(cells) {
		end := start
		for end < len(cells) && cells[end].value == cells[start].value {
			end++
		}
		firstInRow := map[int64]int64{}
		firstInCol := map[int64]int64{}
		for _, x := range cells[start:end] {
			id := x.r*cols + x.c
			if other, ok := firstInRow[x.r]; ok {
				a, b := find(parent, id), find(parent, other)
				parent[a] = b
			} else {
				firstInRow[x.r] = id
			}
			if other, ok := firstInCol[x.c]; ok {
				a, b := find(parent, id), find(parent, other)
				parent[a] = b
			} else {
				firstInCol[x.c] = id
			}
		}
		groupRank := map[int64]int32{}
		for _, x := range cells[start:end] {
			root := find(parent, x.r*cols+x.c)
			rank := max(rowMax[x.r], colMax[x.c]) + 1
			groupRank[root] = max(groupRank[root], rank)
		}
		for _, x := range cells[start:end] {
			rank := groupRank[find(parent, x.r*cols+x.c)]
			answer[x.r][x.c] = rank
			rowMax[x.r] = rank
			colMax[x.c] = rank
		}
		start = end
	}
	return answer
}

var seed int64 = 1632

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	matrices := make([][][]int32, 0, 12)
	for m := 0; m < 12; m++ {
		matrix := make([][]int32, 300)
		for r := range matrix {
			matrix[r] = make([]int32, 300)
			for c := range matrix[r] {
				matrix[r][c] = int32(nextRandom() % 10000)
			}
		}
		matrices = append(matrices, matrix)
	}
	var check, total int64
	for _, matrix := range matrices {
		for _, row := range matrixRankTransform(matrix) {
			for _, rank := range row {
				total += int64(rank)
				check = (check*31 + int64(rank)) % 1000000007
			}
		}
	}
	fmt.Printf("12 matrices of 300 x 300: ranks sum to %d, checksum %d\n", total, check)
}
