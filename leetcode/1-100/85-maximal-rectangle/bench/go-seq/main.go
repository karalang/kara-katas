package main

import "fmt"

func largestRect(heights []int64) int64 {
	n := int64(len(heights))
	stack := make([]int64, 0, n+1)
	var best int64 = 0
	for i := int64(0); i <= n; i++ {
		var h int64 = 0
		if i != n {
			h = heights[i]
		}
		for len(stack) > 0 && heights[stack[len(stack)-1]] >= h {
			top := stack[len(stack)-1]
			height := heights[top]
			stack = stack[:len(stack)-1]
			var width int64
			if len(stack) == 0 {
				width = i
			} else {
				width = i - stack[len(stack)-1] - 1
			}
			area := height * width
			if area > best {
				best = area
			}
		}
		stack = append(stack, i)
	}
	return best
}

func maximalRectangle(matrix [][]int64, rows, cols int64) int64 {
	heights := make([]int64, cols)
	var best int64 = 0
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			if matrix[r][c] == 1 {
				heights[c]++
			} else {
				heights[c] = 0
			}
		}
		a := largestRect(heights)
		if a > best {
			best = a
		}
	}
	return best
}

func main() {
	var rows, cols, passes int64 = 70, 70, 11000

	matrix := make([][]int64, 0, rows)
	var state int64 = 12345
	for r := int64(0); r < rows; r++ {
		rowv := make([]int64, 0, cols)
		for c := int64(0); c < cols; c++ {
			state = (state*1103515245 + 12345) & 2147483647
			if (state>>16)%100 < 62 {
				rowv = append(rowv, 1)
			} else {
				rowv = append(rowv, 0)
			}
		}
		matrix = append(matrix, rowv)
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		rr := p % rows
		cc := (p*131 + 7) % cols
		matrix[rr][cc] = 1 - matrix[rr][cc]
		sink += maximalRectangle(matrix, rows, cols)
	}
	fmt.Println(sink)
}
