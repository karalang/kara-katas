// LeetCode #2146: K Highest Ranked Items Within a Price Range -- the
// benchmark, the same algorithm as ranked.kara.
package main

import (
	"fmt"
	"sort"
)

type item struct{ dist, price, r, c int64 }

func highestRankedKItems(grid [][]int64, low, high, sr, sc int64, k int) [][2]int64 {
	m, n := int64(len(grid)), int64(len(grid[0]))
	seen := make([][]bool, m)
	for i := range seen {
		seen[i] = make([]bool, n)
	}
	seen[sr][sc] = true
	queue := [][3]int64{{sr, sc, 0}}
	head := 0
	var found []item
	dirs := [4][2]int64{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	for head < len(queue) {
		cur := queue[head]
		head++
		r, c, dist := cur[0], cur[1], cur[2]
		price := grid[r][c]
		if price >= low && price <= high {
			found = append(found, item{dist, price, r, c})
		}
		for _, d := range dirs {
			nr, nc := r+d[0], c+d[1]
			if nr >= 0 && nr < m && nc >= 0 && nc < n && !seen[nr][nc] && grid[nr][nc] != 0 {
				seen[nr][nc] = true
				queue = append(queue, [3]int64{nr, nc, dist + 1})
			}
		}
	}
	sort.Slice(found, func(i, j int) bool {
		a, b := found[i], found[j]
		if a.dist != b.dist {
			return a.dist < b.dist
		}
		if a.price != b.price {
			return a.price < b.price
		}
		if a.r != b.r {
			return a.r < b.r
		}
		return a.c < b.c
	})
	if len(found) > k {
		found = found[:k]
	}
	out := make([][2]int64, len(found))
	for i, f := range found {
		out[i] = [2]int64{f.r, f.c}
	}
	return out
}

var seed int64 = 2146

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func draw() int64 {
	if nextRandom()%5 == 0 {
		return 0
	}
	return nextRandom()%99999 + 2
}

func main() {
	grids := make([][][]int64, 4)
	for g := range grids {
		grids[g] = make([][]int64, 316)
		for r := range grids[g] {
			grids[g][r] = make([]int64, 316)
			for c := range grids[g][r] {
				grids[g][r][c] = draw()
			}
		}
	}
	total, check := 0, int64(0)
	for round := int64(0); round < 25; round++ {
		for g := 0; g < 4; g++ {
			r := nextRandom() % 316
			c := nextRandom() % 316
			grids[g][r][c] = draw()
			sr := nextRandom() % 316
			sc := nextRandom() % 316
			if grids[g][sr][sc] == 0 {
				grids[g][sr][sc] = 1
			}
			cells := highestRankedKItems(grids[g], 2, 50000, sr, sc, 1000)
			total += len(cells)
			for _, cell := range cells {
				check = (check*31 + cell[0]*1000 + cell[1] + round) % 1000000007
			}
		}
	}
	fmt.Printf("100 searches: %d items in all, checksum %d\n", total, check)
}
