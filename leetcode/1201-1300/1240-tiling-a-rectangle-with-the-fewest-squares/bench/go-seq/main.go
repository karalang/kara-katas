// LeetCode #1240: the benchmark, mirroring the Kāra file.
package main

import "fmt"

func fill(heights []int64, n, count int64, best *int64) {
	if count >= *best {
		return
	}
	at := 0
	for j := 1; j < len(heights); j++ {
		if heights[j] < heights[at] {
			at = j
		}
	}
	base := heights[at]
	if base == n {
		*best = count
		return
	}
	var width int64
	for at+int(width) < len(heights) && heights[at+int(width)] == base && width < n-base {
		width++
	}
	for size := width; size >= 1; size-- {
		for j := at; j < at+int(size); j++ {
			heights[j] = base + size
		}
		fill(heights, n, count+1, best)
		for j := at; j < at+int(size); j++ {
			heights[j] = base
		}
	}
}

func tilingRectangle(n, m int64) int64 {
	heights := make([]int64, m)
	best := n * m
	fill(heights, n, 0, &best)
	return best
}

func main() {
	var total, check int64
	for pass := 0; pass < 200; pass++ {
		for n := int64(1); n <= 13; n++ {
			for m := int64(1); m <= 13; m++ {
				t := tilingRectangle(n, m)
				total += t
				check = (check*131 + t) % 1000000007
			}
		}
	}
	fmt.Printf("169 rectangles, 200 passes: total %d, checksum %d\n", total, check)
}
