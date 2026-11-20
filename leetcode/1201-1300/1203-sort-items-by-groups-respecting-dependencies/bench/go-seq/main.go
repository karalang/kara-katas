// LeetCode #1203 bench, in Go: the ★ arm (each item in no group given one
// of its own, then Kahn's algorithm over the groups and over the items) on
// four instances of 30000 items drawn once, then 10 rounds over the four,
// each answer folded into a checksum.
package main

import (
	"fmt"
	"slices"
)

var seed int64 = 1203

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func topoSort(nodes int, edges [][]int) []int {
	indegree := make([]int, nodes)
	for _, out := range edges {
		for _, v := range out {
			indegree[v]++
		}
	}
	order := []int{}
	for v := 0; v < nodes; v++ {
		if indegree[v] == 0 {
			order = append(order, v)
		}
	}
	for head := 0; head < len(order); head++ {
		for _, v := range edges[order[head]] {
			indegree[v]--
			if indegree[v] == 0 {
				order = append(order, v)
			}
		}
	}
	if len(order) == nodes {
		return order
	}
	return nil
}

func sortItems(n, m int, group []int, beforeItems [][]int) []int {
	owner := slices.Clone(group)
	groups := m
	for i := range owner {
		if owner[i] < 0 {
			owner[i] = groups
			groups++
		}
	}
	itemEdges := make([][]int, n)
	groupEdges := make([][]int, groups)
	for i := 0; i < n; i++ {
		for _, b := range beforeItems[i] {
			itemEdges[b] = append(itemEdges[b], i)
			if owner[b] != owner[i] {
				groupEdges[owner[b]] = append(groupEdges[owner[b]], owner[i])
			}
		}
	}
	items := topoSort(n, itemEdges)
	ranks := topoSort(groups, groupEdges)
	if items == nil || ranks == nil {
		return nil
	}
	members := make([][]int, groups)
	for _, i := range items {
		members[owner[i]] = append(members[owner[i]], i)
	}
	out := []int{}
	for _, g := range ranks {
		out = append(out, members[g]...)
	}
	return out
}

func dependencies(n int, most int64) [][]int {
	beforeItems := make([][]int, n)
	for i := 1; i < n; i++ {
		for k := nextRandom() % (most + 1); k > 0; k-- {
			hi := nextRandom()
			b := int((hi*32768 + nextRandom()) % int64(i))
			if !slices.Contains(beforeItems[i], b) {
				beforeItems[i] = append(beforeItems[i], b)
			}
		}
	}
	return beforeItems
}

func main() {
	n, m := 30000, 3000
	runs := make([]int, n)
	none := make([]int, n)
	for i := range runs {
		if i%10 == 0 {
			runs[i] = -1
		} else {
			runs[i] = i / 10
		}
		none[i] = -1
	}
	loose := dependencies(n, 3)
	dense := dependencies(n, 6)
	cycle := make([][]int, n)
	for i := range loose {
		cycle[i] = slices.Clone(loose[i])
	}
	cycle[0] = append(cycle[0], n-1)
	if !slices.Contains(cycle[n-1], 0) {
		cycle[n-1] = append(cycle[n-1], 0)
	}
	third := dependencies(n, 3)
	groups := [][]int{runs, runs, none, runs}
	deps := [][][]int{loose, dense, third, cycle}
	var check int64
	for round := 0; round < 10; round++ {
		for k := 0; k < 4; k++ {
			order := sortItems(n, m, groups[k], deps[k])
			check = (check*131 + int64(len(order))) % 1000000007
			for _, i := range order {
				check = (check*131 + int64(i) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("10 rounds over 4 instances of 30000 items: checksum %d\n", check)
}
