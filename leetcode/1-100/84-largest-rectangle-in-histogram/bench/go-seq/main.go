// Benchmark workload — Largest Rectangle in Histogram (LeetCode #84).
// Go mirror of ../largest_rectangle.kara. Each iteration builds a fresh sawtooth
// histogram (heights[j] = (j + iter) % 50, N=2000) as a []int64, runs the
// monotonic-stack largestRectangle (its stack a fresh []int64), and folds the area
// through a rolling polynomial hash. Same N/K.
package main

import "fmt"

func largestRectangle(heights []int64, n int64) int64 {
	stack := make([]int64, 0, n+1)
	var maxArea int64 = 0
	for i := int64(0); i <= n; i++ {
		var h int64 = 0
		if i < n {
			h = heights[i]
		}
		for len(stack) > 0 && heights[stack[len(stack)-1]] > h {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			height := heights[top]
			var width int64
			if len(stack) == 0 {
				width = i
			} else {
				width = i - stack[len(stack)-1] - 1
			}
			area := height * width
			if area > maxArea {
				maxArea = area
			}
		}
		stack = append(stack, i)
	}
	return maxArea
}

func build(n, iter int64) []int64 {
	h := make([]int64, n)
	for j := int64(0); j < n; j++ {
		h[j] = (j + iter) % 50
	}
	return h
}

func main() {
	const n = 2000
	const total = 108000
	const modulus = 1000000007
	var sum int64 = 0
	for k := int64(0); k < total; k++ {
		h := build(n, k)
		area := largestRectangle(h, n)
		sum = (sum*131 + (area + 1)) % modulus
	}
	fmt.Println(sum)
}
