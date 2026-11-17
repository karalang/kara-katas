// LeetCode #2249: Count Lattice Points Inside a Circle -- the benchmark's
// Go mirror of lattice.kara: every point of the box bounding the circles
// tried against them until one holds it.
package main

import "fmt"

func countLatticePoints(circles [][3]int64) int64 {
	left, right := circles[0][0]-circles[0][2], circles[0][0]+circles[0][2]
	bottom, top := circles[0][1]-circles[0][2], circles[0][1]+circles[0][2]
	for _, c := range circles[1:] {
		left = min(left, c[0]-c[2])
		right = max(right, c[0]+c[2])
		bottom = min(bottom, c[1]-c[2])
		top = max(top, c[1]+c[2])
	}
	count := int64(0)
	for px := left; px <= right; px++ {
		for py := bottom; py <= top; py++ {
			for _, c := range circles {
				dx, dy := px-c[0], py-c[1]
				if dx*dx+dy*dy <= c[2]*c[2] {
					count++
					break
				}
			}
		}
	}
	return count
}

var seed int64 = 2249

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	check := int64(0)
	for t := 0; t < 100; t++ {
		circles := make([][3]int64, 200)
		for i := range circles {
			x := nextRandom()%100 + 1
			y := nextRandom()%100 + 1
			r := nextRandom()%min(x, y) + 1
			circles[i] = [3]int64{x, y, r}
		}
		check = (check*31 + countLatticePoints(circles)) % 1000000007
	}
	fmt.Printf("100 cases of 200 circles: checksum %d\n", check)
}
