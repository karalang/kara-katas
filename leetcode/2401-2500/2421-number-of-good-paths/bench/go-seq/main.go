// LeetCode #2421: Number of Good Paths -- the bench, the ★ arm: union-find
// over the nodes in order of value, each value's nodes joined to their
// neighbours no larger and then counted by root.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 2421

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func find(parent []int, x int) int {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func numberOfGoodPaths(vals []int64, edges [][2]int) int64 {
	n := len(vals)
	adj := make([][]int, n)
	for _, e := range edges {
		adj[e[0]] = append(adj[e[0]], e[1])
		adj[e[1]] = append(adj[e[1]], e[0])
	}
	parent := make([]int, n)
	order := make([]int, n)
	for i := range parent {
		parent[i] = i
		order[i] = i
	}
	sort.SliceStable(order, func(a, b int) bool { return vals[order[a]] < vals[order[b]] })
	good := int64(n)
	for i := 0; i < n; {
		j := i
		for j < n && vals[order[j]] == vals[order[i]] {
			j++
		}
		for t := i; t < j; t++ {
			u := order[t]
			for _, v := range adj[u] {
				if vals[v] <= vals[u] {
					ru := find(parent, u)
					rv := find(parent, v)
					parent[ru] = rv
				}
			}
		}
		count := map[int]int64{}
		for t := i; t < j; t++ {
			count[find(parent, order[t])]++
		}
		for _, c := range count {
			good += c * (c - 1) / 2
		}
		i = j
	}
	return good
}

func main() {
	type tree struct {
		vals  []int64
		edges [][2]int
	}
	trees := make([]tree, 0, 10)
	for t := int64(0); t < 10; t++ {
		const n = 30000
		vals := make([]int64, n)
		for i := range vals {
			vals[i] = 1 + nextRandom()%(3+1000*t)
		}
		edges := make([][2]int, 0, n-1)
		for i := 1; i < n; i++ {
			edges = append(edges, [2]int{int(nextRandom() % int64(i)), i})
		}
		trees = append(trees, tree{vals, edges})
	}
	check := int64(0)
	for p := int64(0); p < 20; p++ {
		for _, tr := range trees {
			check = (check*31 + numberOfGoodPaths(tr.vals, tr.edges) + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 trees of 3 * 10^4 nodes: checksum %d\n", check)
}
