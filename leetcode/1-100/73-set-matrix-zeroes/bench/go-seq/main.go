// Benchmark workload — Set Matrix Zeroes (LeetCode #73).
// Go single-threaded mirror of bench/set_matrix_zeroes.{kara,rs,c}. Faithful to
// the kata's Vec-of-Vec matrix: each row is an []int64 grown by append and the
// matrix is a [][]int64 grown by append — NOT a fixed [N][N]int64 — so the
// comparison measures the same growing-dynamic-array discipline as Kāra's
// `Vec.new()+push` (the #72 fairness lesson). O(1)-space first-row/col marker
// algorithm, K=100_000 iters over a 20×20 matrix with three punched zeros.
// See ../README.md § Benchmarks.

package main

import "fmt"

func setZeroes(m [][]int64) {
	rows := len(m)
	if rows == 0 {
		return
	}
	cols := len(m[0])

	firstRowZero := false
	firstColZero := false
	for j := 0; j < cols; j++ {
		if m[0][j] == 0 {
			firstRowZero = true
		}
	}
	for i := 0; i < rows; i++ {
		if m[i][0] == 0 {
			firstColZero = true
		}
	}

	for i := 1; i < rows; i++ {
		for j := 1; j < cols; j++ {
			if m[i][j] == 0 {
				m[i][0] = 0
				m[0][j] = 0
			}
		}
	}

	for i := 1; i < rows; i++ {
		for j := 1; j < cols; j++ {
			if m[i][0] == 0 || m[0][j] == 0 {
				m[i][j] = 0
			}
		}
	}

	if firstRowZero {
		for j := 0; j < cols; j++ {
			m[0][j] = 0
		}
	}
	if firstColZero {
		for i := 0; i < rows; i++ {
			m[i][0] = 0
		}
	}
}

func main() {
	const total int64 = 100000
	const modulus int64 = 1000000007
	const rows int64 = 20
	const cols int64 = 20

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		var m [][]int64
		for i := int64(0); i < rows; i++ {
			var row []int64
			for j := int64(0); j < cols; j++ {
				row = append(row, 1+(i*31+j*17+k)%9)
			}
			m = append(m, row)
		}
		m[k%rows][k%cols] = 0
		m[(k*7)%rows][(k*13)%cols] = 0
		m[(k*3)%rows][(k*11)%cols] = 0

		setZeroes(m)

		for i := int64(0); i < rows; i++ {
			for j := int64(0); j < cols; j++ {
				acc = (acc*131 + m[i][j]) % modulus
			}
		}
	}
	fmt.Println(acc)
}
