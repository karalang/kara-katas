// LeetCode #2250: Count Number of Rectangles Containing Each Point -- the
// benchmark's Go mirror of rectangles.kara: rectangles bucketed by height,
// each bucket's lengths sorted, a point summing over the buckets of height
// y to 100 how many lengths are at least x (sort.Search).
package main

import (
	"fmt"
	"slices"
	"sort"
)

func countRectangles(rectangles, points [][2]int64) []int64 {
	byHeight := make([][]int64, 101)
	for _, r := range rectangles {
		byHeight[r[1]] = append(byHeight[r[1]], r[0])
	}
	for _, lengths := range byHeight {
		slices.Sort(lengths)
	}
	counts := make([]int64, 0, len(points))
	for _, p := range points {
		var count int64
		for h := p[1]; h < 101; h++ {
			lengths := byHeight[h]
			count += int64(len(lengths) - sort.Search(len(lengths), func(i int) bool { return lengths[i] >= p[0] }))
		}
		counts = append(counts, count)
	}
	return counts
}

var seed int64 = 2250

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	var check int64
	for t := 0; t < 4; t++ {
		rectangles := make([][2]int64, 50000)
		for i := range rectangles {
			l := wideRandom()%1000000000 + 1
			h := nextRandom()%100 + 1
			rectangles[i] = [2]int64{l, h}
		}
		points := make([][2]int64, 50000)
		for i := range points {
			x := wideRandom()%1000000000 + 1
			y := nextRandom()%100 + 1
			points[i] = [2]int64{x, y}
		}
		for _, c := range countRectangles(rectangles, points) {
			check = (check*31 + c) % 1000000007
		}
	}
	fmt.Printf("4 cases of 5 * 10^4 rectangles and points: checksum %d\n", check)
}
