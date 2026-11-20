// LeetCode #1273 bench, in Go: the ★ arm (the children listed from the
// parents, then a depth-first search returning each subtree's sum and the
// nodes it keeps) on 20 random trees of 10,000 nodes with values from -3
// to 3, drawn once, 60 rounds; every answer folded into a checksum.
package main

import "fmt"

func subtree(node int64, children [][]int64, value []int64) (int64, int64) {
	sum, kept := value[node], int64(1)
	for _, child := range children[node] {
		s, k := subtree(child, children, value)
		sum += s
		kept += k
	}
	if sum == 0 {
		return 0, 0
	}
	return sum, kept
}

func deleteTreeNodes(nodes int64, parent, value []int64) int64 {
	children := make([][]int64, nodes)
	for i := int64(1); i < nodes; i++ {
		children[parent[i]] = append(children[parent[i]], i)
	}
	_, kept := subtree(0, children, value)
	return kept
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomParents(n, reach int64, seed *int64) []int64 {
	order := make([]int64, n)
	for i := range order {
		order[i] = int64(i)
	}
	for i := n - 1; i >= 2; i-- {
		j := 1 + nextRandom(seed)%i
		order[i], order[j] = order[j], order[i]
	}
	parent := make([]int64, n)
	parent[0] = -1
	for i := int64(1); i < n; i++ {
		back := 1 + nextRandom(seed)%min(reach, i)
		parent[order[i]] = order[i-back]
	}
	return parent
}

func main() {
	seed := int64(1273)
	parents := make([][]int64, 20)
	values := make([][]int64, 20)
	for t := range parents {
		parents[t] = randomParents(10000, 1000, &seed)
		values[t] = make([]int64, 10000)
		for i := range values[t] {
			values[t][i] = nextRandom(&seed)%7 - 3
		}
	}
	var check int64
	for round := int64(0); round < 60; round++ {
		for t := range parents {
			check = (check*131 + deleteTreeNodes(10000, parents[t], values[t]) + round) % 1000000007
		}
	}
	fmt.Printf("60 rounds of 20 trees of 10000 nodes: checksum %d\n", check)
}
