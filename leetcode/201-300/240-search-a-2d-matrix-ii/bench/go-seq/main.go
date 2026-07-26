// Benchmark harness for LeetCode #240 — Search a 2D Matrix II.
// Mirrors search_matrix.kara algorithm-for-algorithm.
package main

import "fmt"

func searchMatrix(flat []int64, rows int64, cols int64, target int64) bool {
	if rows == 0 || cols == 0 {
		return false
	}
	r := int64(0)
	c := cols - 1
	for r < rows && c >= 0 {
		v := flat[r*cols+c]
		if v == target {
			return true
		} else if v > target {
			c--
		} else {
			r++
		}
	}
	return false
}

const (
	Rows  = 1000
	Cols  = 1000
	Iters = 120000
)

func main() {
	flat := make([]int64, 0, Rows*Cols)
	for r := int64(0); r < Rows; r++ {
		for c := int64(0); c < Cols; c++ {
			flat = append(flat, r*3+c*5)
		}
	}
	maxv := int64((Rows-1)*3 + (Cols-1)*5)

	var sink int64
	x := int64(12345)
	for it := int64(0); it < Iters; it++ {
		x = (x*1103515245 + 12345) % 2147483648
		target := (x / 65536) % (maxv + 2)
		if searchMatrix(flat, Rows, Cols, target) {
			sink = (sink + it + 1) % 1000000007
		}
	}
	fmt.Println(sink)
}
