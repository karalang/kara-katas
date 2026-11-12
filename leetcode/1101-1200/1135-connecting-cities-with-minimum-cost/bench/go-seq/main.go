// LeetCode #1135: Connecting Cities With Minimum Cost -- the bench in Go,
// the same algorithm and workload as minimum_cost.kara: each road its own
// []int64, the roads copied one by one and sorted with `sort.Slice` in
// every call, the same 8 networks and 50 rounds.
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

func minimumCost(n int64, connections [][]int64) int64 {
	roads := make([][]int64, len(connections))
	for i, c := range connections {
		roads[i] = append([]int64(nil), c...)
	}
	sort.Slice(roads, func(i, j int) bool { return roads[i][2] < roads[j][2] })
	parent := make([]int64, n+1)
	size := make([]int64, n+1)
	for i := range parent {
		parent[i] = int64(i)
		size[i] = 1
	}
	var total int64
	var joined int64 = 1
	for _, road := range roads {
		a := find(parent, road[0])
		b := find(parent, road[1])
		if a != b {
			if size[a] < size[b] {
				a, b = b, a
			}
			parent[b] = a
			size[a] += size[b]
			total += road[2]
			joined++
		}
	}
	if joined == n {
		return total
	}
	return -1
}

var seed int64 = 1135

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	networks := make([][][]int64, 0, 8)
	for j := 0; j < 8; j++ {
		roads := make([][]int64, 0, 10000)
		for i := 0; i < 10000; i++ {
			x := nextRandom()%1000 + 1
			y := nextRandom()%999 + 1
			if y >= x {
				y++
			}
			high := nextRandom()
			roads = append(roads, []int64{x, y, (high*32768+nextRandom())%100000 + 1})
		}
		networks = append(networks, roads)
	}
	var total, check int64
	for round := int64(0); round < 50; round++ {
		for j := int64(0); j < 8; j++ {
			at := (round*7919 + j*104729) % 10000
			networks[j][at][2] = (networks[j][at][2]*7+13)%100000 + 1
			r := minimumCost(1000, networks[j])
			total += r
			check = (check*31 + r + 1) % 1000000007
		}
	}
	fmt.Printf("50 rounds over 8 networks of 1000 cities and 10000 roads: costs total %d, checksum %d\n", total, check)
}
