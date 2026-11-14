// LeetCode #2132: Stamping the Grid -- the benchmark, the same algorithm
// as stamp.kara.
package main

import "fmt"

func possibleToStamp(grid [][]int64, stampHeight, stampWidth int64) bool {
	m := int64(len(grid))
	n := int64(len(grid[0]))
	w := n + 1
	full := make([]int64, (m+1)*w)
	for r := int64(0); r < m; r++ {
		for c := int64(0); c < n; c++ {
			full[(r+1)*w+c+1] = grid[r][c] + full[r*w+c+1] + full[(r+1)*w+c] - full[r*w+c]
		}
	}
	marks := make([]int64, (m+1)*w)
	for r := int64(0); r < m-stampHeight+1; r++ {
		for c := int64(0); c < n-stampWidth+1; c++ {
			r2, c2 := r+stampHeight, c+stampWidth
			if full[r2*w+c2]-full[r*w+c2]-full[r2*w+c]+full[r*w+c] == 0 {
				marks[r*w+c]++
				marks[r*w+c2]--
				marks[r2*w+c]--
				marks[r2*w+c2]++
			}
		}
	}
	for r := int64(0); r < m; r++ {
		for c := int64(0); c < n; c++ {
			if r > 0 {
				marks[r*w+c] += marks[(r-1)*w+c]
			}
			if c > 0 {
				marks[r*w+c] += marks[r*w+c-1]
			}
			if r > 0 && c > 0 {
				marks[r*w+c] -= marks[(r-1)*w+c-1]
			}
			if grid[r][c] == 0 && marks[r*w+c] == 0 {
				return false
			}
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2132)
	grid := make([][]int64, 400)
	for r := 0; r < 400; r++ {
		grid[r] = make([]int64, 500)
		for c := 0; c < 500; c++ {
			if r%4 == 3 || c%4 == 3 {
				grid[r][c] = 1
			}
		}
	}
	stamped, check := int64(0), int64(0)
	for round := int64(0); round < 100; round++ {
		hi := nextRandom(&seed)
		at := (hi*32768 + nextRandom(&seed)) % 200000
		r, c := at/500, at%500
		grid[r][c] = 1 - grid[r][c]
		h := nextRandom(&seed)%3 + 1
		w := nextRandom(&seed)%3 + 1
		fits := int64(0)
		if possibleToStamp(grid, h, w) {
			fits = 1
		}
		grid[r][c] = 1 - grid[r][c]
		stamped += fits
		check = (check*31 + fits + at + round) % 1000000007
	}
	fmt.Printf("100 solves: %d stamped, checksum %d\n", stamped, check)
}
