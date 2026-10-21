// Benchmark for #836: Rectangle Overlap -- the ★ arm (the two projections).
//
// Mirrors is_rectangle_overlap.kara: two axis-aligned rectangles overlap
// with positive area exactly when their shadows on the x axis overlap in
// more than a point and so do their shadows on the y axis.
package main

import "fmt"

func isRectangleOverlap(rec1, rec2 []int64) bool {
	left := max(rec1[0], rec2[0])
	right := min(rec1[2], rec2[2])
	bottom := max(rec1[1], rec2[1])
	top := min(rec1[3], rec2[3])
	return left < right && bottom < top
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

// a number below 2^32, from three draws
func bigRandom(seed *int64) int64 {
	hi := nextRandom(seed) * 32768
	hi += nextRandom(seed)
	return hi*4 + nextRandom(seed)%4
}

func main() {
	// 4096 rectangles drawn once in LeetCode's range, their corners
	// anywhere and their sides up to 2 * 10^9 >> (k % 8) for rectangle k,
	// so they run from the size of the range down to a 128th of it.
	// Round s tests each rectangle i against rectangle (i + s + 1) % 4096.
	n := int64(4096)
	rounds := int64(100000)
	seed := int64(836)
	rects := make([][]int64, 0)
	for k := int64(0); k < n; k++ {
		reach := int64(2000000000) >> (k % 8)
		x1 := bigRandom(&seed)%2000000000 - 1000000000
		y1 := bigRandom(&seed)%2000000000 - 1000000000
		x2 := min(x1+1+bigRandom(&seed)%reach, 1000000000)
		y2 := min(y1+1+bigRandom(&seed)%reach, 1000000000)
		rects = append(rects, []int64{x1, y1, x2, y2})
	}
	total := int64(0)
	checksum := int64(0)
	for s := int64(0); s < rounds; s++ {
		overlapping := int64(0)
		for i := int64(0); i < n; i++ {
			if isRectangleOverlap(rects[i], rects[(i+s+1)%n]) {
				overlapping++
			}
		}
		total += overlapping
		checksum = (checksum*131 + overlapping) % 1000000007
	}
	fmt.Printf("%d rounds of %d pairs: %d overlapping, checksum %d\n", rounds, n, total, checksum)
}
