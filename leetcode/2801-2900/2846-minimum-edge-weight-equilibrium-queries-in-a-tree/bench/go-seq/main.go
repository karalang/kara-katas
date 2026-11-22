// LeetCode #2846: Minimum Edge Weight Equilibrium Queries in a Tree --
// the bench, mirrored from equilibrium.kara: weight counts from the
// root by a breadth-first walk, and each query's lowest common ancestor
// by binary lifting.
package main

import "fmt"

type edge struct{ to, w int }

func minOperationsQueries(n int, edges [][3]int, queries [][2]int) []int64 {
	adj := make([][]edge, n)
	for _, e := range edges {
		adj[e[0]] = append(adj[e[0]], edge{e[1], e[2]})
		adj[e[1]] = append(adj[e[1]], edge{e[0], e[2]})
	}
	const levels = 15
	up := make([][]int, levels)
	for j := range up {
		up[j] = make([]int, n)
	}
	depth := make([]int64, n)
	count := make([][]int64, n)
	count[0] = make([]int64, 27)
	seen := make([]bool, n)
	queue := []int{0}
	seen[0] = true
	for len(queue) > 0 {
		v := queue[0]
		queue = queue[1:]
		for _, e := range adj[v] {
			if !seen[e.to] {
				seen[e.to] = true
				up[0][e.to] = v
				depth[e.to] = depth[v] + 1
				count[e.to] = append([]int64(nil), count[v]...)
				count[e.to][e.w]++
				queue = append(queue, e.to)
			}
		}
	}
	for j := 1; j < levels; j++ {
		for v := 0; v < n; v++ {
			up[j][v] = up[j-1][up[j-1][v]]
		}
	}
	lca := func(a, b int) int {
		x, y := a, b
		if depth[a] < depth[b] {
			x, y = b, a
		}
		for j := levels - 1; j >= 0; j-- {
			if depth[x]-(1<<j) >= depth[y] {
				x = up[j][x]
			}
		}
		if x == y {
			return x
		}
		for j := levels - 1; j >= 0; j-- {
			if up[j][x] != up[j][y] {
				x = up[j][x]
				y = up[j][y]
			}
		}
		return up[0][x]
	}
	answers := make([]int64, 0, len(queries))
	for _, q := range queries {
		a, b := q[0], q[1]
		c := lca(a, b)
		onPath := make([]int64, 0, 26)
		for w := 1; w < 27; w++ {
			onPath = append(onPath, count[a][w]+count[b][w]-2*count[c][w])
		}
		var sum, most int64
		for _, x := range onPath {
			sum += x
			if x > most {
				most = x
			}
		}
		answers = append(answers, sum-most)
	}
	return answers
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, n, asked, rounds = 10, 10000, 20000, 5
	seed := int64(2846)
	type caseT struct {
		edges   [][3]int
		queries [][2]int
	}
	cases := make([]caseT, 0, count)
	for c := 0; c < count; c++ {
		label := make([]int, n)
		for i := range label {
			label[i] = i
		}
		for i := n - 1; i >= 1; i-- {
			j := int(nextRandom(&seed) % int64(i+1))
			label[i], label[j] = label[j], label[i]
		}
		edges := make([][3]int, 0, n-1)
		for i := 1; i < n; i++ {
			a := label[i]
			b := label[nextRandom(&seed)%int64(i)]
			edges = append(edges, [3]int{a, b, int(nextRandom(&seed)%26 + 1)})
		}
		queries := make([][2]int, 0, asked)
		for i := 0; i < asked; i++ {
			a := int(nextRandom(&seed) % n)
			queries = append(queries, [2]int{a, int(nextRandom(&seed) % n)})
		}
		cases = append(cases, caseT{edges, queries})
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, cs := range cases {
			for _, ops := range minOperationsQueries(n, cs.edges, cs.queries) {
				total += ops
				check = (check*31 + ops + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d trees of %d, %d queries, %d rounds: %d operations, checksum %d\n", count, n, asked, rounds, total, check)
}
