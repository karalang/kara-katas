// LeetCode 766 — Toeplitz Matrix: benchmark, the ★ arm in Go.
// Sixteen 200 by 200 Toeplitz matrices, built once; 30,000 rounds of
// changing one cell, asking, and putting it back.
package main

import "fmt"

var seed int64 = 766

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func isToeplitzMatrix(matrix [][]int64) bool {
	for i := 1; i < len(matrix); i++ {
		for j := 1; j < len(matrix[i]); j++ {
			if matrix[i][j] != matrix[i-1][j-1] {
				return false
			}
		}
	}
	return true
}

func main() {
	const size = 200
	rounds := 30000
	pool := make([][][]int64, 16)
	for k := range pool {
		diag := make([]int64, 2*size-1)
		for d := range diag {
			diag[d] = nextRandom() % 10
		}
		pool[k] = make([][]int64, size)
		for i := 0; i < size; i++ {
			pool[k][i] = make([]int64, size)
			for j := 0; j < size; j++ {
				pool[k][i][j] = diag[i-j+size-1]
			}
		}
	}
	var yes, check int64
	for round := 0; round < rounds; round++ {
		k := round % 16
		i := nextRandom() % size
		j := nextRandom() % size
		old := pool[k][i][j]
		pool[k][i][j] = old + nextRandom()%2
		answer := isToeplitzMatrix(pool[k])
		pool[k][i][j] = old
		if answer {
			yes++
		}
		a := int64(0)
		if answer {
			a = 1
		}
		check = (check*31 + a + i*size + j) % 1000000007
	}
	fmt.Printf("%d rounds on 200 by 200: %d Toeplitz, checksum %d\n", rounds, yes, check)
}
