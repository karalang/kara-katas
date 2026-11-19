// LeetCode #1637: Widest Vertical Area Between Two Points Containing No
// Points -- the bench's Go mirror: the ★ arm on 40 random sets of 100000
// points with x and y from 0 to 10^9, all drawn first.
package main

import (
	"fmt"
	"slices"
)

func maxWidthOfVerticalArea(points [][]int32) int32 {
	xs := make([]int32, len(points))
	for i, p := range points {
		xs[i] = p[0]
	}
	slices.Sort(xs)
	var widest int32
	for i := 1; i < len(xs); i++ {
		widest = max(widest, xs[i]-xs[i-1])
	}
	return widest
}

var seed int64 = 1637

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	sets := make([][][]int32, 40)
	for s := range sets {
		points := make([][]int32, 100000)
		for i := range points {
			x := (nextRandom()*32768 + nextRandom()) % 1000000001
			y := (nextRandom()*32768 + nextRandom()) % 1000000001
			points[i] = []int32{int32(x), int32(y)}
		}
		sets[s] = points
	}
	var check, total int64
	for _, points := range sets {
		width := int64(maxWidthOfVerticalArea(points))
		total += width
		check = (check*31 + width + 1) % 1000000007
	}
	fmt.Printf("40 sets of 100000 points: widths sum to %d, checksum %d\n", total, check)
}
