// LeetCode #2280: Minimum Lines to Represent a Line Chart -- the bench,
// the ★ arm.
package main

import (
	"fmt"
	"sort"
)

func minimumLines(stockPrices [][]int64) int64 {
	points := make([][]int64, len(stockPrices))
	copy(points, stockPrices)
	sort.Slice(points, func(a, b int) bool { return points[a][0] < points[b][0] })
	n := len(points)
	if n < 2 {
		return 0
	}
	var lines int64 = 1
	for i := 2; i < n; i++ {
		a, b, c := points[i-2], points[i-1], points[i]
		if (b[1]-a[1])*(c[0]-b[0]) != (c[1]-b[1])*(b[0]-a[0]) {
			lines++
		}
	}
	return lines
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2280

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 20; t++ {
		points := make([][]int64, 0)
		var day, price int64 = 1, 500000000
		for len(points) < 100000 {
			dx := nextRandom()%1000 + 1
			dy := nextRandom()%2001 - 1000
			run := nextRandom()%5 + 1
			for r := int64(0); r < run; r++ {
				if len(points) < 100000 {
					points = append(points, []int64{day, price})
					day += dx
					price += dy
				}
			}
		}
		for i := 99999; i >= 1; i-- {
			high := nextRandom()
			j := (high*32768 + nextRandom()) % int64(i+1)
			points[i], points[j] = points[j], points[i]
		}
		check = (check*31 + minimumLines(points)) % 1000000007
	}
	fmt.Printf("20 charts of 10^5: checksum %d\n", check)
}
