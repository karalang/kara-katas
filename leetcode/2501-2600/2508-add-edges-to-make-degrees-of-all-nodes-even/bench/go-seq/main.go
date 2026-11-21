// LeetCode #2508: Add Edges to Make Degrees of All Nodes Even -- Go
// mirror of the benchmark (even.kara): the same graphs, passes and
// checksum, the edges held in a map.
package main

import "fmt"

func isPossible(n int64, edges [][2]int64) bool {
	degree := make([]int64, n+1)
	present := make(map[int64]struct{})
	code := func(a, b int64) int64 { return min(a, b)*(n+1) + max(a, b) }
	for _, e := range edges {
		degree[e[0]]++
		degree[e[1]]++
		present[code(e[0], e[1])] = struct{}{}
	}
	free := func(a, b int64) bool { _, ok := present[code(a, b)]; return !ok }
	var odd []int64
	for v := int64(1); v <= n; v++ {
		if degree[v]%2 == 1 {
			odd = append(odd, v)
		}
	}
	switch len(odd) {
	case 0:
		return true
	case 2:
		a, b := odd[0], odd[1]
		if free(a, b) {
			return true
		}
		for c := int64(1); c <= n; c++ {
			if c != a && c != b && free(a, c) && free(b, c) {
				return true
			}
		}
		return false
	case 4:
		a, b, c, d := odd[0], odd[1], odd[2], odd[3]
		return (free(a, b) && free(c, d)) || (free(a, c) && free(b, d)) || (free(a, d) && free(b, c))
	}
	return false
}

func ringOf(n, step int64) [][2]int64 {
	edges := make([][2]int64, 0, n)
	for v := int64(1); v <= n; v++ {
		edges = append(edges, [2]int64{v, (v+step-1)%n + 1})
	}
	return edges
}

func joinedRing(spare int64) [][2]int64 {
	var edges [][2]int64
	for v := int64(3); v < 33000; v++ {
		edges = append(edges, [2]int64{v, v + 1})
	}
	edges = append(edges, [2]int64{33000, 3}, [2]int64{1, 2})
	for v := int64(3); v <= 33000; v++ {
		if v != spare {
			for h := int64(1); h <= 2; h++ {
				edges = append(edges, [2]int64{h, v})
			}
		}
	}
	return edges
}

type graph struct {
	n     int64
	edges [][2]int64
}

func main() {
	const passes = 90
	graphs := []graph{{100000, ringOf(100000, 1)}, {100000, ringOf(100000, 2)}, {33000, joinedRing(0)}, {33000, joinedRing(17000)}}
	var check int64
	for p := int64(0); p < passes; p++ {
		for i := range graphs {
			g := &graphs[i]
			at := check % int64(len(g.edges))
			taken := g.edges[at]
			last := len(g.edges) - 1
			g.edges[at] = g.edges[last]
			g.edges = g.edges[:last]
			answer := int64(1)
			if isPossible(g.n, g.edges) {
				answer = 2
			}
			check = (check*31 + answer + p) % 1000000007
			g.edges = append(g.edges, taken)
			g.edges[at], g.edges[last] = g.edges[last], g.edges[at]
		}
	}
	fmt.Printf("%d passes over 4 graphs: checksum %d\n", passes, check)
}
