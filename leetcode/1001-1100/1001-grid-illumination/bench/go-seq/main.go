// Benchmark: LeetCode #1001 Grid Illumination -- the ★ arm, counts per
// line in hash maps, on grids of 10^9 by 10^9 with 20000 lamps and 20000
// queries, LeetCode's largest. Mirrors grid_illumination.kara, .c, .rs and
// .py.
package main

import "fmt"

func gridIllumination(n int64, lamps [][]int64, queries [][]int64) []int64 {
	on := map[int64]bool{}
	rows := map[int64]int64{}
	cols := map[int64]int64{}
	diags := map[int64]int64{}
	antis := map[int64]int64{}
	for _, lamp := range lamps {
		r, c := lamp[0], lamp[1]
		if !on[r*n+c] {
			on[r*n+c] = true
			rows[r]++
			cols[c]++
			diags[r-c]++
			antis[r+c]++
		}
	}
	ans := []int64{}
	for _, q := range queries {
		r, c := q[0], q[1]
		lit := rows[r] > 0 || cols[c] > 0 || diags[r-c] > 0 || antis[r+c] > 0
		if lit {
			ans = append(ans, 1)
		} else {
			ans = append(ans, 0)
		}
		for i := r - 1; i < r+2; i++ {
			for j := c - 1; j < c+2; j++ {
				if i >= 0 && i < n && j >= 0 && j < n && on[i*n+j] {
					delete(on, i*n+j)
					rows[i]--
					cols[j]--
					diags[i-j]--
					antis[i+j]--
				}
			}
		}
	}
	return ans
}

var seed int64 = 1001

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func bigRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func main() {
	rounds := 1
	var n int64 = 1000000000
	// 20 cases, each with 20000 lamps in a window of 100000 by 100000
	// cells at a random place in the grid, and 20000 queries, half of them
	// anywhere in the window and half on or beside a random lamp
	allLamps := [][][]int64{}
	allQueries := [][][]int64{}
	for t := 0; t < 20; t++ {
		top := 1 + bigRandom()%(n-100002)
		left := 1 + bigRandom()%(n-100002)
		lamps := [][]int64{}
		for x := 0; x < 20000; x++ {
			r := top + bigRandom()%100000
			c := left + bigRandom()%100000
			lamps = append(lamps, []int64{r, c})
		}
		queries := [][]int64{}
		for q := 0; q < 20000; q++ {
			if q%2 == 0 {
				r := top + bigRandom()%100000
				c := left + bigRandom()%100000
				queries = append(queries, []int64{r, c})
			} else {
				lamp := lamps[nextRandom()%20000]
				r := lamp[0] + nextRandom()%3 - 1
				queries = append(queries, []int64{r, lamp[1] + nextRandom()%3 - 1})
			}
		}
		allLamps = append(allLamps, lamps)
		allQueries = append(allQueries, queries)
	}
	var lit, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			k := (r + i) % 20
			for _, a := range gridIllumination(n, allLamps[k], allQueries[k]) {
				lit += a
				check = (check*31 + a + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over 20 grids of 20000 lamps and 20000 queries: %d lit, checksum %d\n", rounds, lit, check)
}
