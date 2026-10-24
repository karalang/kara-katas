// Benchmark: LeetCode #947 Most Stones Removed with Same Row or Column --
// the ★ arm, rows and columns joined, on sets of 1000 stones, LeetCode's
// largest. Mirrors remove_stones.kara, .c, .rs and .py.
package main

import "fmt"

func findLine(parent []int64, v int64) int64 {
	x := v
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func removeStones(stones [][]int64) int64 {
	parent := make([]int64, 20002)
	for v := range parent {
		parent[v] = -1
	}
	var groups int64
	for _, s := range stones {
		row := s[0]
		col := 10001 + s[1]
		if parent[row] < 0 {
			parent[row] = row
			groups++
		}
		if parent[col] < 0 {
			parent[col] = col
			groups++
		}
		a := findLine(parent, row)
		b := findLine(parent, col)
		if a != b {
			parent[a] = b
			groups--
		}
	}
	return int64(len(stones)) - groups
}

var seed int64 = 947

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count, n := 1000, 20, 1000
	sets := make([][][]int64, 0, count)
	for c := 0; c < count; c++ {
		side := 200 + nextRandom()%1801
		taken := make(map[int64]bool)
		stones := make([][]int64, 0, n)
		for len(stones) < n {
			x := nextRandom() % side
			y := nextRandom() % side
			if !taken[x*10001+y] {
				taken[x*10001+y] = true
				stones = append(stones, []int64{x, y})
			}
		}
		sets = append(sets, stones)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			m := removeStones(sets[(r+i)%count])
			total += m
			check = (check*1000003 + m) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d sets of %d stones: %d removed, checksum %d\n", rounds, count, n, total, check)
}
