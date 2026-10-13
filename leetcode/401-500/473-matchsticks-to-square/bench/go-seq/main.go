// Benchmark for #473: Go mirror of the ★ arm (backtracking, longest
// stick first); see ../matchsticks.kara.
package main

import (
	"fmt"
	"sort"
)

func place(sticks []int64, i int, sides *[4]int64, side int64) bool {
	if i == len(sticks) {
		return true
	}
	for s := 0; s < 4; s++ {
		if sides[s]+sticks[i] > side {
			continue
		}
		repeat := false
		for t := 0; t < s; t++ {
			if sides[t] == sides[s] {
				repeat = true
				break
			}
		}
		if repeat {
			continue
		}
		sides[s] += sticks[i]
		if place(sticks, i+1, sides, side) {
			return true
		}
		sides[s] -= sticks[i]
	}
	return false
}

func makesquare(matchsticks []int64) bool {
	if len(matchsticks) < 4 {
		return false
	}
	var total int64
	for _, m := range matchsticks {
		total += m
	}
	if total%4 != 0 {
		return false
	}
	side := total / 4
	sticks := append([]int64(nil), matchsticks...)
	sort.Slice(sticks, func(a, b int) bool { return sticks[a] > sticks[b] })
	if sticks[0] > side {
		return false
	}
	var sides [4]int64
	return place(sticks, 0, &sides, side)
}

var seed int64 = 473

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	cases := 2000
	squares := 0
	var checksum int64
	for c := 0; c < cases; c++ {
		sticks := make([]int64, 0, 15)
		var total int64
		for i := 0; i < 15; i++ {
			v := 50 + nextRandom()%50
			sticks = append(sticks, v)
			total += v
		}
		sticks[14] += (4 - total%4) % 4
		ok := makesquare(sticks)
		if ok {
			squares++
		}
		var bit int64 = 2
		if ok {
			bit = 1
		}
		checksum = (checksum*3 + bit) % 1000000007
	}
	fmt.Printf("%d sets of 15 sticks: %d squares, checksum %d\n", cases, squares, checksum)
}
