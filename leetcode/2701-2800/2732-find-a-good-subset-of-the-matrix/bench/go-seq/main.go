// LeetCode #2732: Find a Good Subset of the Matrix -- the bench
// (subset.kara in Go): a row of zeros alone, or the first rows of two
// disjoint masks among the 32.
package main

import "fmt"

func goodSubsetofBinaryMatrix(grid [][]int64) []int64 {
	var first [32]int64
	for k := range first {
		first[k] = -1
	}
	for i, row := range grid {
		var mask int64
		for j, x := range row {
			mask |= x << j
		}
		if mask == 0 {
			return []int64{int64(i)}
		}
		if first[mask] < 0 {
			first[mask] = int64(i)
		}
	}
	for a := 1; a < 32; a++ {
		for b := a + 1; b < 32; b++ {
			if a&b == 0 && first[a] >= 0 && first[b] >= 0 {
				return []int64{min(first[a], first[b]), max(first[a], first[b])}
			}
		}
	}
	return []int64{}
}

var seed int64 = 2732

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const grids, m, n, rounds = 100, 10000, 5, 10
	all := [][][]int64{}
	for g := 0; g < grids; g++ {
		kind := g % 3
		column := nextRandom() % n
		free := nextRandom() % m
		grid := make([][]int64, 0, m)
		for r := int64(0); r < m; r++ {
			row := make([]int64, 0, n)
			for j := 0; j < n; j++ {
				row = append(row, nextRandom()%2)
			}
			if kind == 1 || (kind == 2 && r != free) {
				row[column] = 1
			}
			grid = append(grid, row)
		}
		all = append(all, grid)
	}
	var found, check int64
	for r := int64(0); r < rounds; r++ {
		for _, grid := range all {
			rows := goodSubsetofBinaryMatrix(grid)
			if len(rows) > 0 {
				found++
			}
			var named int64
			for _, x := range rows {
				named += x
			}
			check = (check*31 + named + int64(len(rows)) + r) % 1000000007
		}
	}
	fmt.Printf("%d grids of %d rows, %d rounds: %d good subsets found, checksum %d\n", grids, m, rounds, found, check)
}
