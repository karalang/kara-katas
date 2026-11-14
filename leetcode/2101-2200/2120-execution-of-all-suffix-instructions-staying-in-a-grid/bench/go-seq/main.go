// LeetCode #2120: Execution of All Suffix Instructions Staying in a Grid
// -- the benchmark, the same algorithm as suffix.kara: each suffix
// simulated, 40 grids built once, 20 rounds with every start one row
// lower than in the round before.

package main

import "fmt"

func executeInstructions(n int64, startPos []int64, s []byte) []int64 {
	m := len(s)
	answer := make([]int64, 0, m)
	for i := 0; i < m; i++ {
		row, col, count := startPos[0], startPos[1], int64(0)
		for j := i; j < m; j++ {
			switch s[j] {
			case 'L':
				col--
			case 'R':
				col++
			case 'U':
				row--
			default:
				row++
			}
			if row < 0 || row >= n || col < 0 || col >= n {
				break
			}
			count++
		}
		answer = append(answer, count)
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

type grid struct {
	n, row, col int64
	s           []byte
}

func main() {
	seed := int64(2120)
	grids := make([]grid, 0, 40)
	for g := 0; g < 40; g++ {
		n := nextRandom(&seed)%401 + 100
		row := nextRandom(&seed) % n
		col := nextRandom(&seed) % n
		s := make([]byte, 0, 500)
		for k := 0; k < 500; k++ {
			s = append(s, "LRUD"[nextRandom(&seed)%4])
		}
		grids = append(grids, grid{n, row, col, s})
	}
	var total, check int64
	for round := int64(0); round < 20; round++ {
		for _, g := range grids {
			start := []int64{(g.row + round) % g.n, g.col}
			for _, c := range executeInstructions(g.n, start, g.s) {
				total += c
				check = (check*31 + c) % 1000000007
			}
		}
	}
	fmt.Printf("800 solves: %d moves, checksum %d\n", total, check)
}
