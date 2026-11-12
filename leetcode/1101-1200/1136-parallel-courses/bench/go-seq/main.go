// LeetCode #1136: Parallel Courses -- the bench, the ★ arm's algorithm:
// Kahn's algorithm a semester at a time.
package main

import "fmt"

func minimumSemesters(n int64, relations [][]int64) int64 {
	after := make([][]int64, n+1)
	need := make([]int64, n+1)
	for _, r := range relations {
		after[r[0]] = append(after[r[0]], r[1])
		need[r[1]]++
	}
	var now []int64
	for c := int64(1); c <= n; c++ {
		if need[c] == 0 {
			now = append(now, c)
		}
	}
	var semesters, taken int64
	for len(now) > 0 {
		semesters++
		taken += int64(len(now))
		var upcoming []int64
		for _, c := range now {
			for _, d := range after[c] {
				need[d]--
				if need[d] == 0 {
					upcoming = append(upcoming, d)
				}
			}
		}
		now = upcoming
	}
	if taken == n {
		return semesters
	}
	return -1
}

var seed int64 = 1136

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 5000
	plans := make([][][]int64, 0, 8)
	for j := 0; j < 8; j++ {
		relations := make([][]int64, 0)
		for c := int64(2); c <= n; c++ {
			relations = append(relations, []int64{nextRandom()%(c-1) + 1, c})
		}
		plans = append(plans, relations)
	}
	var total, check int64
	for round := int64(0); round < 300; round++ {
		for j := int64(0); j < 8; j++ {
			at := (round*7919 + j*104729) % (n - 1)
			c := plans[j][at][1]
			plans[j][at][0] = nextRandom()%(c-1) + 1
			r := minimumSemesters(n, plans[j])
			total += r
			check = (check*31 + r + 1) % 1000000007
		}
	}
	fmt.Printf("300 rounds over 8 plans of 5000 courses and 4999 relations: semesters total %d, checksum %d\n", total, check)
}
