// LeetCode #685: Redundant Connection II -- union-find and two
// candidates. Bench.
//
// 100 random rooted trees of 20,000 vertices, each with one more directed
// edge, are built once; then 30 rounds answer every graph.
package main

import "fmt"

type edge struct{ a, b int64 }

func find(parent []int64, x int64) int64 {
	v := x
	for parent[v] != v {
		parent[v] = parent[parent[v]]
		v = parent[v]
	}
	return v
}

func findRedundantDirectedConnection(edges []edge) edge {
	n := int64(len(edges))
	into := make([]int64, n+1)
	for v := range into {
		into[v] = -1
	}
	first, second := int64(-1), int64(-1)
	for i, e := range edges {
		if into[e.b] == -1 {
			into[e.b] = int64(i)
		} else {
			first = into[e.b]
			second = int64(i)
		}
	}
	parent := make([]int64, n+1)
	for v := int64(0); v <= n; v++ {
		parent[v] = v
	}
	for i, e := range edges {
		if int64(i) != second {
			ra := find(parent, e.a)
			rb := find(parent, e.b)
			if ra == rb {
				if first == -1 {
					return e
				}
				return edges[first]
			}
			parent[rb] = ra
		}
	}
	return edges[second]
}

var seed int64 = 685

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n, rounds int64 = 100, 20000, 30
	graphs := make([][]edge, 0, count)
	for c := int64(0); c < count; c++ {
		name := make([]int64, n)
		for v := int64(0); v < n; v++ {
			name[v] = v + 1
		}
		for i := n - 1; i > 0; i-- {
			j := nextRandom() % (i + 1)
			name[i], name[j] = name[j], name[i]
		}
		up := make([]int64, n+1)
		edges := make([]edge, 0, n)
		for v := int64(1); v < n; v++ {
			a := name[nextRandom()%v]
			up[name[v]] = a
			edges = append(edges, edge{a, name[v]})
		}
		for {
			a := 1 + nextRandom()%n
			b := 1 + nextRandom()%n
			if a != b && up[b] != a {
				edges = append(edges, edge{a, b})
				break
			}
		}
		for k := n - 1; k > 0; k-- {
			j := nextRandom() % (k + 1)
			edges[k], edges[j] = edges[j], edges[k]
		}
		graphs = append(graphs, edges)
	}
	var sum int64
	for r := int64(0); r < rounds; r++ {
		for c := int64(0); c < count; c++ {
			e := findRedundantDirectedConnection(graphs[c])
			sum = (sum*31 + e.a*20011 + e.b + r) % 1000000007
		}
	}
	fmt.Printf("%d graphs answered, checksum %d\n", count*rounds, sum)
}
