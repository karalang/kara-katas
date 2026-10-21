// Benchmark for #834: Sum of Distances in Tree -- the ★ arm (rerooting, with a stack).
//
// Mirrors sum_of_distances_in_tree.kara: one walk from node 0 on an
// explicit stack records parents and a visiting order; the order taken
// backwards gives subtree sizes and distance sums, and taken forwards
// moves the root along each edge.
package main

import "fmt"

type edge struct{ a, b int64 }

func sumOfDistancesInTree(n int64, edges []edge) []int64 {
	adj := make([][]int64, 0)
	for i := int64(0); i < n; i++ {
		adj = append(adj, nil)
	}
	for _, e := range edges {
		adj[e.a] = append(adj[e.a], e.b)
		adj[e.b] = append(adj[e.b], e.a)
	}
	parent := make([]int64, n)
	for i := range parent {
		parent[i] = -1
	}
	order := make([]int64, 0)
	seen := make([]bool, n)
	stack := []int64{0}
	seen[0] = true
	for len(stack) > 0 {
		u := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		order = append(order, u)
		for _, v := range adj[u] {
			if !seen[v] {
				seen[v] = true
				parent[v] = u
				stack = append(stack, v)
			}
		}
	}
	size := make([]int64, n)
	down := make([]int64, n)
	for i := range size {
		size[i] = 1
	}
	for j := int64(0); j < n; j++ {
		u := order[n-1-j]
		p := parent[u]
		if p >= 0 {
			size[p] += size[u]
			down[p] += down[u] + size[u]
		}
	}
	answer := make([]int64, n)
	answer[0] = down[0]
	for _, u := range order {
		p := parent[u]
		if p >= 0 {
			answer[u] = answer[p] - size[u] + (n - size[u])
		}
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 16 trees drawn once, each of LeetCode's largest size, 30000 nodes:
	// node v > 0 hangs from a node among the `reach` before it, `reach`
	// running from 2 to 2^16 over the trees, with the labels shuffled.
	// Each round solves the next tree and reads one answer.
	count := int64(16)
	rounds := int64(320)
	n := int64(30000)
	seed := int64(834)
	trees := make([][]edge, 0)
	for g := int64(0); g < count; g++ {
		reach := int64(2) << g
		label := make([]int64, n)
		for i := range label {
			label[i] = int64(i)
		}
		i := n
		for i > 1 {
			j := nextRandom(&seed) % i
			i--
			label[i], label[j] = label[j], label[i]
		}
		edges := make([]edge, 0)
		for v := int64(1); v < n; v++ {
			lo := int64(0)
			if v > reach {
				lo = v - reach
			}
			u := lo + nextRandom(&seed)%(v-lo)
			edges = append(edges, edge{label[u], label[v]})
		}
		trees = append(trees, edges)
	}
	total := int64(0)
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		answer := sumOfDistancesInTree(n, trees[round%count])
		x := answer[round*7919%n]
		total += x
		checksum = (checksum*131 + x) % 1000000007
	}
	fmt.Printf("%d rounds of %d trees: answers total %d, checksum %d\n", rounds, count, total, checksum)
}
