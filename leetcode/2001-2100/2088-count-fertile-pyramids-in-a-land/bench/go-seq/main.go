// LeetCode #2088: Count Fertile Pyramids in a Land -- Go mirror of the ★
// arm's benchmark (pyramids.kara): the same 20 lands, each counted 20 times
// by the same two passes over slices.
package main

import "fmt"

var seed int64 = 2088

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func countOneWay(grid [][]int64, order []int) int64 {
	n := len(grid[0])
	below := make([]int64, n)
	var count int64
	for _, r := range order {
		tall := make([]int64, n)
		for c := 0; c < n; c++ {
			if grid[r][c] == 0 {
				continue
			}
			if c == 0 || c == n-1 {
				tall[c] = 1
			} else {
				tall[c] = min(below[c-1], below[c], below[c+1]) + 1
			}
			count += tall[c] - 1
		}
		below = tall
	}
	return count
}

func countPyramids(grid [][]int64) int64 {
	m := len(grid)
	up := make([]int, m)
	down := make([]int, m)
	for i := 0; i < m; i++ {
		up[i] = m - 1 - i
		down[i] = i
	}
	return countOneWay(grid, up) + countOneWay(grid, down)
}

func main() {
	lands := make([][][]int64, 0, 20)
	for t := int64(0); t < 20; t++ {
		odds := 15 + t%5
		land := make([][]int64, 316)
		for r := range land {
			land[r] = make([]int64, 316)
			for c := range land[r] {
				if nextRandom()%20 < odds {
					land[r][c] = 1
				}
			}
		}
		lands = append(lands, land)
	}
	var total, check int64
	for round := 0; round < 20; round++ {
		for t := 0; t < 20; t++ {
			a := countPyramids(lands[(t+round)%20])
			total += a
			check = (check*31 + a) % 1000000007
		}
	}
	fmt.Printf("400 counts: sum %d, checksum %d\n", total, check)
}
