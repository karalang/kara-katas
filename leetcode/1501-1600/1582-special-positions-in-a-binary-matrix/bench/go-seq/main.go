// LeetCode #1582 bench: the same row and column sums, in Go.
package main

import "fmt"

func numSpecial(mat [][]int64) int64 {
	m, n := len(mat), len(mat[0])
	rows := make([]int64, m)
	cols := make([]int64, n)
	for i, row := range mat {
		for _, x := range row {
			rows[i] += x
		}
	}
	for j := 0; j < n; j++ {
		for i := 0; i < m; i++ {
			cols[j] += mat[i][j]
		}
	}
	var count int64
	for i, row := range mat {
		for j := 0; j < n; j++ {
			if row[j] == 1 && rows[i] == 1 && cols[j] == 1 {
				count++
			}
		}
	}
	return count
}

var seed int64 = 1582

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	mats := make([][][]int64, 0, 2000)
	for p := 0; p < 2000; p++ {
		mat := make([][]int64, 0, 100)
		for i := 0; i < 100; i++ {
			row := make([]int64, 0, 100)
			for j := 0; j < 100; j++ {
				if nextRandom()%100 == 0 {
					row = append(row, 1)
				} else {
					row = append(row, 0)
				}
			}
			mat = append(mat, row)
		}
		mats = append(mats, mat)
	}
	var check, total int64
	for _, mat := range mats {
		special := numSpecial(mat)
		total += special
		check = mix(check, special)
	}
	fmt.Printf("2000 matrices of 100 x 100: special positions %d, checksum %d\n", total, check)
}
