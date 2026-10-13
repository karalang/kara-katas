// Benchmark for #498: Go mirror of the ★ arm (walking the zigzag); see
// ../diagonal_traverse.kara.
package main

import "fmt"

func findDiagonalOrder(mat [][]int64) []int64 {
	m := len(mat)
	n := len(mat[0])
	out := []int64{}
	r, c := 0, 0
	up := true
	for len(out) < m*n {
		out = append(out, mat[r][c])
		if up {
			if c == n-1 {
				r++
				up = false
			} else if r == 0 {
				c++
				up = false
			} else {
				r--
				c++
			}
		} else {
			if r == m-1 {
				c++
				up = true
			} else if c == 0 {
				r++
				up = true
			} else {
				r++
				c--
			}
		}
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 100 matrices of 10,000 cells (the problem's most), in ten shapes
	// from 1 by 10,000 to 10,000 by 1, with values from -100,000 to
	// 100,000, built once. Then each is traversed 100 times; every
	// traversal is folded into the checksum, each value weighed by its
	// place.
	rows := []int{1, 4, 10, 25, 50, 100, 200, 400, 1000, 10000}
	var seed int64 = 498
	all := [][][]int64{}
	for k := 0; k < 100; k++ {
		m := rows[k%10]
		n := 10000 / m
		mat := [][]int64{}
		for i := 0; i < m; i++ {
			row := []int64{}
			for j := 0; j < n; j++ {
				row = append(row, nextRandom(&seed)%200001-100000)
			}
			mat = append(mat, row)
		}
		all = append(all, mat)
	}
	var checksum int64
	for t := 0; t < 100; t++ {
		for k := 0; k < 100; k++ {
			order := findDiagonalOrder(all[k])
			var s int64
			for i, v := range order {
				s += v * int64(i%7+1)
			}
			checksum = (checksum*31 + s%1000000007 + 1000000007) % 1000000007
		}
	}
	fmt.Printf("100 matrices of 10000 cells, 100 times each: checksum %d\n", checksum)
}
