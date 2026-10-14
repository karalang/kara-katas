// Benchmark for #593: Go mirror of the ★ arm (the six distances, sorted);
// see ../valid_square.kara. The distances go into a slice each call,
// sorted with slices.Sort.
package main

import (
	"fmt"
	"slices"
)

func dist(a, b []int64) int64 {
	dx := a[0] - b[0]
	dy := a[1] - b[1]
	return dx*dx + dy*dy
}

func validSquare(p1, p2, p3, p4 []int64) bool {
	d := []int64{dist(p1, p2), dist(p1, p3), dist(p1, p4), dist(p2, p3), dist(p2, p4), dist(p3, p4)}
	slices.Sort(d)
	return d[0] > 0 && d[0] == d[3] && d[4] == d[5] && d[4] == 2*d[0]
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomPoints(seed *int64) [][]int64 {
	kind := step(seed) % 3
	points := [][]int64{}
	if kind == 2 {
		for k := 0; k < 4; k++ {
			x := step(seed)%7 - 3
			y := step(seed)%7 - 3
			points = append(points, []int64{x, y})
		}
		return points
	}
	x := step(seed)%2001 - 1000
	y := step(seed)%2001 - 1000
	dx := step(seed)%41 - 20
	dy := step(seed)%41 - 20
	if dx == 0 && dy == 0 {
		dx = 1
	}
	points = append(points, []int64{x, y}, []int64{x + dx, y + dy}, []int64{x + dx - dy, y + dy + dx}, []int64{x - dy, y + dx})
	if kind == 1 {
		k := step(seed) % 4
		c := step(seed) % 2
		if step(seed)%2 == 0 {
			points[k][c]++
		} else {
			points[k][c]--
		}
	}
	for k := int64(0); k < 3; k++ {
		j := k + step(seed)%(4-k)
		points[k], points[j] = points[j], points[k]
	}
	return points
}

func main() {
	count, rounds := 1000, 20000
	seed := int64(593)
	cases := [][][]int64{}
	for k := 0; k < count; k++ {
		cases = append(cases, randomPoints(&seed))
	}
	var squares, checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			p := cases[(round*7+g)%count]
			if validSquare(p[0], p[1], p[2], p[3]) {
				squares++
				checksum = (checksum*31 + int64(g) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d cases, %d rounds: %d squares, checksum %d\n", count, rounds, squares, checksum)
}
