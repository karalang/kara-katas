// LeetCode #2397: Maximum Rows Covered by Columns -- the bench, the ★ arm
// in Go: each row as the mask of its 1s, every mask of numSelect columns
// tried.
package main

import (
	"fmt"
	"math/bits"
)

var seed int64 = 2397

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func grid(m, n, odds int64) [][]int64 {
	g := make([][]int64, m)
	for r := range g {
		g[r] = make([]int64, n)
		for c := range g[r] {
			if nextRandom()%odds == 0 {
				g[r][c] = 1
			}
		}
	}
	return g
}

func maximumRows(matrix [][]int64, numSelect int64) int64 {
	n := len(matrix[0])
	masks := make([]int64, len(matrix))
	for r, row := range matrix {
		var mask int64
		for c := 0; c < n; c++ {
			if row[c] == 1 {
				mask |= 1 << c
			}
		}
		masks[r] = mask
	}
	var best int64
	for chosen := int64(0); chosen < 1<<n; chosen++ {
		if int64(bits.OnesCount64(uint64(chosen))) != numSelect {
			continue
		}
		var covered int64
		for _, mask := range masks {
			if mask&chosen == mask {
				covered++
			}
		}
		if covered > best {
			best = covered
		}
	}
	return best
}

func main() {
	grids := make([][][]int64, 200)
	for g := range grids {
		grids[g] = grid(12, 12, 2+int64(g)%4)
	}
	var check int64
	for p := int64(0); p < 10; p++ {
		for _, g := range grids {
			for k := int64(1); k < 13; k++ {
				check = (check*31 + maximumRows(g, k) + p) % 1000000007
			}
		}
	}
	fmt.Printf("10 passes over 200 grids of 12 by 12, every choice: checksum %d\n", check)
}
