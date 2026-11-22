// LeetCode #2858: Minimum Edge Reversals So Every Node Is Reachable --
// the bench: the ★ arm over 20 random trees of 10^5 nodes, LeetCode's
// most, every other one deep, labels shuffled and each edge pointing
// either way, all drawn first, then each answered 5 times.
package main

import "fmt"

type arc struct{ to, w int64 }

func minEdgeReversals(n int64, edges [][2]int64) []int64 {
	adj := make([][]arc, n)
	for _, e := range edges {
		adj[e[0]] = append(adj[e[0]], arc{e[1], 0})
		adj[e[1]] = append(adj[e[1]], arc{e[0], 1})
	}
	parent := make([]int64, n)
	for i := range parent {
		parent[i] = -1
	}
	cost := make([]int64, n)
	order := make([]int64, 0, n)
	stack := []int64{0}
	parent[0] = 0
	var root int64
	for len(stack) > 0 {
		u := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		order = append(order, u)
		for _, a := range adj[u] {
			if parent[a.to] == -1 {
				parent[a.to] = u
				cost[a.to] = a.w
				root += a.w
				stack = append(stack, a.to)
			}
		}
	}
	answer := make([]int64, n)
	answer[0] = root
	for _, u := range order[1:] {
		if cost[u] == 0 {
			answer[u] = answer[parent[u]] + 1
		} else {
			answer[u] = answer[parent[u]] - 1
		}
	}
	return answer
}

var seed int64 = 2858

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func tree(n int64, deep bool) [][2]int64 {
	label := make([]int64, n)
	for i := range label {
		label[i] = int64(i)
	}
	for i := n - 1; i >= 1; i-- {
		j := wide() % (i + 1)
		label[i], label[j] = label[j], label[i]
	}
	edges := make([][2]int64, 0, n-1)
	for i := int64(1); i < n; i++ {
		var p int64
		if deep {
			p = i - 1 - nextRandom()%min(i, 3)
		} else {
			p = wide() % i
		}
		if nextRandom()%2 == 0 {
			edges = append(edges, [2]int64{label[p], label[i]})
		} else {
			edges = append(edges, [2]int64{label[i], label[p]})
		}
	}
	return edges
}

func main() {
	const count, rounds, n = 20, 5, 100000
	trees := make([][][2]int64, count)
	for c := 0; c < count; c++ {
		trees[c] = tree(n, c%2 == 1)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, edges := range trees {
			for _, a := range minEdgeReversals(n, edges) {
				total += a
				check = (check*31 + a + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d trees of %d, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, total, check)
}
