// LeetCode #1595: Minimum Cost to Connect Two Groups of Points
// -- the bench in Go, mirroring connect.kara: one edge per first point
// over a mask of the second group's points joined, then each point still
// alone takes its cheapest edge; 200 problems of 12 by 12, costs from 0
// to 100, all drawn first.
package main

import (
	"fmt"
	"math"
)

var seed int64 = 1595

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func connectTwoGroups(cost [][]int32) int32 {
	first, second := len(cost), len(cost[0])
	full := 1 << second
	cheapest := make([]int32, second)
	for j := 0; j < second; j++ {
		cheapest[j] = cost[0][j]
		for i := 1; i < first; i++ {
			cheapest[j] = min(cheapest[j], cost[i][j])
		}
	}
	best := make([]int32, full)
	for m := range best {
		best[m] = math.MaxInt32
	}
	best[0] = 0
	for i := 0; i < first; i++ {
		next := make([]int32, full)
		for m := range next {
			next[m] = math.MaxInt32
		}
		for mask := 0; mask < full; mask++ {
			if best[mask] == math.MaxInt32 {
				continue
			}
			for j := 0; j < second; j++ {
				joined := mask | 1<<j
				next[joined] = min(next[joined], best[mask]+cost[i][j])
			}
		}
		best = next
	}
	var answer int32 = math.MaxInt32
	for mask := 0; mask < full; mask++ {
		if best[mask] == math.MaxInt32 {
			continue
		}
		total := best[mask]
		for j := 0; j < second; j++ {
			if mask>>j&1 == 0 {
				total += cheapest[j]
			}
		}
		answer = min(answer, total)
	}
	return answer
}

func main() {
	problems := make([][][]int32, 200)
	for p := range problems {
		problems[p] = make([][]int32, 12)
		for r := range problems[p] {
			problems[p][r] = make([]int32, 12)
			for c := range problems[p][r] {
				problems[p][r][c] = int32(nextRandom() % 101)
			}
		}
	}
	var check, total int64
	for _, cost := range problems {
		answer := connectTwoGroups(cost)
		total += int64(answer)
		check = (check*31 + int64(answer) + 1) % 1000000007
	}
	fmt.Printf("200 problems of 12 by 12: total %d, checksum %d\n", total, check)
}
