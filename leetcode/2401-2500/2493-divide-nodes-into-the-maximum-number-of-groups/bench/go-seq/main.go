// LeetCode #2493: Divide Nodes Into the Maximum Number of Groups -- Go
// mirror of the benchmark (groups.kara): the same graph, passes and
// checksum; adjacency slices built on every ask, a breadth-first search
// from every node.
package main

import "fmt"

var seed int64 = 2493

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func magnificentSets(n int64, edges [][2]int64) int64 {
	next := make([][]int64, n+1)
	for _, e := range edges {
		next[e[0]] = append(next[e[0]], e[1])
		next[e[1]] = append(next[e[1]], e[0])
	}
	most := make([]int64, n+1)
	for start := int64(1); start <= n; start++ {
		depth := make([]int64, n+1)
		for i := range depth {
			depth[i] = -1
		}
		depth[start] = 0
		queue := []int64{start}
		head := 0
		least, deepest := start, int64(0)
		for head < len(queue) {
			node := queue[head]
			head++
			if node < least {
				least = node
			}
			if depth[node] > deepest {
				deepest = depth[node]
			}
			for _, other := range next[node] {
				if depth[other] == -1 {
					depth[other] = depth[node] + 1
					queue = append(queue, other)
				} else if depth[other] == depth[node] {
					return -1
				}
			}
		}
		if deepest+1 > most[least] {
			most[least] = deepest + 1
		}
	}
	var sum int64
	for _, x := range most {
		sum += x
	}
	return sum
}

func main() {
	const n int64 = 500
	const passes int64 = 38
	side := make([]int64, n+1)
	for v := int64(1); v <= n; v++ {
		side[v] = nextRandom() % 2
	}
	taken := map[int64]bool{}
	var edges [][2]int64
	for i := 0; i < 8000; i++ {
		a := nextRandom()%n + 1
		b := nextRandom()%n + 1
		lo, hi := min(a, b), max(a, b)
		if a != b && side[a] != side[b] && !taken[lo*1000+hi] {
			taken[lo*1000+hi] = true
			edges = append(edges, [2]int64{a, b})
		}
	}
	m := int64(len(edges))
	var check int64
	for p := int64(0); p < passes; p++ {
		asked := append([][2]int64(nil), edges[:m-check%100]...)
		check = (check*31 + magnificentSets(n, asked) + p) % 1000000007
	}
	fmt.Printf("%d passes over 500 nodes and %d edges: checksum %d\n", passes, m, check)
}
