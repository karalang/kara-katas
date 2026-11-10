// Benchmark: LeetCode #1101 The Earliest Moment When Everyone Become
// Friends -- union-find over the logs in time order, as the Kāra ★ arm.
// Mirrors ../earliest_acq.kara; each call copies every log.
package main

import (
	"fmt"
	"sort"
)

func find(parent []int64, x int64) int64 {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func earliestAcq(logs [][]int64, n int64) int64 {
	copied := make([][]int64, len(logs))
	for i, log := range logs {
		copied[i] = append([]int64(nil), log...)
	}
	sort.Slice(copied, func(i, j int) bool { return copied[i][0] < copied[j][0] })
	parent := make([]int64, n)
	size := make([]int64, n)
	for i := range parent {
		parent[i] = int64(i)
		size[i] = 1
	}
	groups := n
	for _, log := range copied {
		a, b := find(parent, log[1]), find(parent, log[2])
		if a == b {
			continue
		}
		big, small := a, b
		if size[a] < size[b] {
			big, small = b, a
		}
		parent[small] = big
		size[big] += size[small]
		groups--
		if groups == 1 {
			return log[0]
		}
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1101)
	groups := make([][][]int64, 0, 64)
	for g := 0; g < 64; g++ {
		times := make([]int64, 4950)
		for i := range times {
			times[i] = int64(i)
		}
		for i := 4949; i >= 1; i-- {
			j := nextRandom(&seed) % int64(i+1)
			times[i], times[j] = times[j], times[i]
		}
		logs := make([][]int64, 0, 4950)
		for x := int64(0); x < 100; x++ {
			for y := x + 1; y < 100; y++ {
				logs = append(logs, []int64{times[len(logs)] * 1000, x, y})
			}
		}
		groups = append(groups, logs)
	}
	var total, check int64
	for round := int64(0); round < 20; round++ {
		for j := int64(0); j < 64; j++ {
			a := (round*7919 + j*104729) % 4950
			b := (round*31 + j*17 + 1) % 4950
			groups[j][a][0], groups[j][b][0] = groups[j][b][0], groups[j][a][0]
			moment := earliestAcq(groups[j], 100)
			total += moment
			check = (check*31 + moment + 2) % 1000000007
		}
	}
	fmt.Printf("20 rounds over 64 groups of 100 people: moments sum to %d, checksum %d\n", total, check)
}
