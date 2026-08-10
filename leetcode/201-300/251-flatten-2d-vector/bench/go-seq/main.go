// Benchmark workload for LeetCode #251 — Flatten 2D Vector (Go mirror).
// Mirrors flatten_2d.kara algorithm-for-algorithm.
package main

import "fmt"

type Vector2D struct {
	data [][]int64
	row  int
	col  int
}

func (v *Vector2D) skipEmpty() {
	for v.row < len(v.data) && v.col >= len(v.data[v.row]) {
		v.row++
		v.col = 0
	}
}

func (v *Vector2D) hasNext() bool {
	v.skipEmpty()
	return v.row < len(v.data)
}

func (v *Vector2D) next() int64 {
	v.skipEmpty()
	if v.row >= len(v.data) {
		return -1
	}
	x := v.data[v.row][v.col]
	v.col++
	return x
}

func main() {
	var rows int64 = 20000
	var passes int64 = 1500

	data := make([][]int64, 0, rows)
	var state int64 = 251251
	for r := int64(0); r < rows; r++ {
		state = (state*1103515245 + 12345) & 2147483647
		row := []int64{}
		if (state/65536)%100 >= 45 {
			state = (state*1103515245 + 12345) & 2147483647
			cols := (state/65536)%6 + 1
			for c := int64(0); c < cols; c++ {
				state = (state*1103515245 + 12345) & 2147483647
				row = append(row, (state/65536)%1000)
			}
		}
		data = append(data, row)
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		v := Vector2D{data: data, row: 0, col: 0}
		for v.hasNext() {
			x := v.next()
			sink = (sink*31 + x + 1) % 1000000007
		}
	}
	fmt.Println(sink)
}
