// Bench mirror of spiral_bench.kara — boundary-shrinking spiral over a batch of LCG-filled
// 24x24 matrices, position-weighted checksum folded into an int64 sink. go build.
// See ../../README.md § Benchmarks.
package main

import "fmt"

func main() {
	var m int64 = 1103515245       // glibc LCG multiplier
	var inc int64 = 12345          // glibc LCG increment
	var modulus int64 = 2147483648 // 2^31
	var windows int64 = 200000     // number of simulated input matrices
	var rows int64 = 24
	var cols int64 = 24
	var n int64 = 576 // rows * cols

	var grid [576]int64
	var state int64 = 1 // LCG seed
	var sink int64 = 0
	for k := int64(0); k < windows; k++ {
		for idx := int64(0); idx < n; idx++ {
			state = (state*m + inc) % modulus
			grid[idx] = (state % 100) - 50
		}
		var local int64 = 0
		var pos int64 = 0
		top, bottom, left, right := int64(0), rows-1, int64(0), cols-1
		for top <= bottom && left <= right {
			for c := left; c <= right; c++ {
				local += (pos + 1) * grid[top*cols+c]
				pos++
			}
			top++
			for r := top; r <= bottom; r++ {
				local += (pos + 1) * grid[r*cols+right]
				pos++
			}
			right--
			if top <= bottom {
				for c2 := right; c2 >= left; c2-- {
					local += (pos + 1) * grid[bottom*cols+c2]
					pos++
				}
				bottom--
			}
			if left <= right {
				for r2 := bottom; r2 >= top; r2-- {
					local += (pos + 1) * grid[r2*cols+left]
					pos++
				}
				left++
			}
		}
		sink += local
	}
	fmt.Println(sink)
}
