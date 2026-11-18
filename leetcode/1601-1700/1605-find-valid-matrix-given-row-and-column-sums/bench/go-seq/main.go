// LeetCode #1605: Find Valid Matrix Given Row and Column Sums -- the bench
// in Go, mirroring restore.kara: greedy, cell by cell in reading order.
package main

import "fmt"

func restoreMatrix(rowSum, colSum []int32) [][]int32 {
	rows := append([]int32(nil), rowSum...)
	cols := append([]int32(nil), colSum...)
	m := make([][]int32, 0, len(rows))
	for i := range rows {
		row := make([]int32, len(cols))
		for j := range cols {
			x := rows[i]
			if cols[j] < x {
				x = cols[j]
			}
			row[j] = x
			rows[i] -= x
			cols[j] -= x
		}
		m = append(m, row)
	}
	return m
}

var seed int64 = 1605

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type problem struct{ rows, cols []int32 }
	var problems []problem
	for p := 0; p < 100; p++ {
		rows := make([]int32, 1000)
		cols := make([]int32, 1000)
		for i := 0; i < 1000; i++ {
			for j := 0; j < 1000; j++ {
				x := int32(nextRandom() % 1001)
				rows[i] += x
				cols[j] += x
			}
		}
		problems = append(problems, problem{rows, cols})
	}
	var check, nonzero int64
	for _, p := range problems {
		for _, row := range restoreMatrix(p.rows, p.cols) {
			for _, x := range row {
				if x != 0 {
					nonzero++
					check = (check*31 + int64(x) + 1) % 1000000007
				}
			}
		}
	}
	fmt.Printf("100 problems of 1000 by 1000: %d cells not zero, checksum %d\n", nonzero, check)
}
