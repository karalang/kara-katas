// LeetCode #2467: Most Profitable Path in a Tree -- the bench, the ★ arm in
// Go: breadth-first parents and depths from node 0 over slice adjacency
// lists, Bob's seconds up his parent chain, and each node's income its
// parent's plus its gate.
package main

import (
	"fmt"
	"math"
)

func mostProfitablePath(edges [][2]int64, bob int64, amount []int64) int64 {
	n := int64(len(amount))
	adjacent := make([][]int64, n)
	for _, e := range edges {
		adjacent[e[0]] = append(adjacent[e[0]], e[1])
		adjacent[e[1]] = append(adjacent[e[1]], e[0])
	}
	parent := make([]int64, n)
	for i := range parent {
		parent[i] = -1
	}
	depth := make([]int64, n)
	order := []int64{0}
	parent[0] = 0
	for next := 0; next < len(order); next++ {
		node := order[next]
		for _, child := range adjacent[node] {
			if parent[child] < 0 {
				parent[child] = node
				depth[child] = depth[node] + 1
				order = append(order, child)
			}
		}
	}
	bobTime := make([]int64, n)
	for i := range bobTime {
		bobTime[i] = n
	}
	node := bob
	var t int64
	for node != 0 {
		bobTime[node] = t
		node = parent[node]
		t++
	}
	bobTime[0] = t
	income := make([]int64, n)
	best := int64(math.MinInt64)
	for _, v := range order {
		var gate int64
		if depth[v] < bobTime[v] {
			gate = amount[v]
		} else if depth[v] == bobTime[v] {
			gate = amount[v] / 2
		}
		if v == 0 {
			income[v] = gate
		} else {
			income[v] = income[parent[v]] + gate
		}
		if v != 0 && len(adjacent[v]) == 1 && income[v] > best {
			best = income[v]
		}
	}
	return best
}

var seed int64 = 2467

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 10 random trees of 10^4 nodes built once, each node joined to an
	// earlier one, with even amounts from -10^4 to 10^4; then 140
	// passes, each moving every tree's Bob and setting one amount from the
	// checksum so far, then answering it and folding the answer plus the
	// pass into the checksum
	const n = 10000
	trees := [][][2]int64{}
	amounts := [][]int64{}
	for a := 0; a < 10; a++ {
		edges := [][2]int64{}
		for node := int64(1); node < n; node++ {
			r := nextRandom()
			edges = append(edges, [2]int64{node, (r*32768 + nextRandom()) % node})
		}
		trees = append(trees, edges)
		amount := make([]int64, n)
		for i := range amount {
			amount[i] = 2*(nextRandom()%10001) - 10000
		}
		amounts = append(amounts, amount)
	}
	var check int64
	for p := int64(0); p < 140; p++ {
		for a := range trees {
			bob := 1 + check%(n-1)
			amounts[a][(check+int64(a))%n] = 2*(check%10001) - 10000
			got := mostProfitablePath(trees[a], bob, amounts[a])
			check = ((check*31+got+p)%1000000007 + 1000000007) % 1000000007
		}
	}
	fmt.Printf("140 passes over 10 trees of 10^4: checksum %d\n", check)
}
