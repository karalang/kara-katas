// LeetCode #2768: Number of Black Blocks -- the bench in Go: the ★ arm
// over 100 grids of 10^4 black cells, all drawn first, then each answered
// 5 times. The blocks in a map keyed by the top-left corner.
package main

import (
	"fmt"
	"strings"
)

func countBlackBlocks(m, n int64, coordinates [][]int64) []int64 {
	blocks := map[[2]int64]int64{}
	for _, cell := range coordinates {
		x, y := cell[0], cell[1]
		for bx := max(x-1, 0); bx <= min(x, m-2); bx++ {
			for by := max(y-1, 0); by <= min(y, n-2); by++ {
				blocks[[2]int64{bx, by}]++
			}
		}
	}
	counts := make([]int64, 5)
	for _, black := range blocks {
		counts[black]++
	}
	counts[0] = (m-1)*(n-1) - int64(len(blocks))
	return counts
}

var seed int64 = 2768

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

type grid struct {
	m, n  int64
	cells [][]int64
}

func main() {
	count := 100
	rounds := 5
	grids := make([]grid, 0, count)
	for c := 0; c < count; c++ {
		side := wide()%900 + 101
		area := side * side
		m := side + wide()%(100001-side)
		n := side + wide()%(100001-side)
		x0 := wide() % (m - side + 1)
		y0 := wide() % (n - side + 1)
		stride := wide() % area
		for gcd(stride, area) != 1 {
			stride = wide() % area
		}
		start := wide() % area
		cells := make([][]int64, 10000)
		for k := int64(0); k < 10000; k++ {
			at := (start + k*stride) % area
			cells[k] = []int64{x0 + at/side, y0 + at%side}
		}
		grids = append(grids, grid{m, n, cells})
	}
	sums := make([]int64, 5)
	var check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, g := range grids {
			counts := countBlackBlocks(g.m, g.n, g.cells)
			for i := 0; i < 5; i++ {
				sums[i] += counts[i]
				check = (check*31 + counts[i]%1000000007 + r + 1) % 1000000007
			}
		}
	}
	parts := make([]string, 5)
	for i, s := range sums {
		parts[i] = fmt.Sprint(s)
	}
	fmt.Printf("%d grids of 10^4 cells, %d rounds: counts sum to [%s], checksum %d\n", count, rounds, strings.Join(parts, ", "), check)
}
