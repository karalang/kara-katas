// LeetCode #1129: Shortest Path with Alternating Colors -- the bench in Go,
// the ★ arm over [][]int64 edge lists: the adjacency built per call as one
// slice per node and colour, a breadth-first search over (node, colour)
// with a slice queue, the same 32 graphs and 1000 rounds.
package main

import "fmt"

type state struct{ node, colour int64 }

func shortestAlternatingPaths(n int64, redEdges, blueEdges [][]int64) []int64 {
	adj := [2][][]int64{make([][]int64, n), make([][]int64, n)}
	for _, e := range redEdges {
		adj[0][e[0]] = append(adj[0][e[0]], e[1])
	}
	for _, e := range blueEdges {
		adj[1][e[0]] = append(adj[1][e[0]], e[1])
	}
	dist := [2][]int64{make([]int64, n), make([]int64, n)}
	for i := int64(0); i < n; i++ {
		dist[0][i] = -1
		dist[1][i] = -1
	}
	dist[0][0] = 0
	dist[1][0] = 0
	queue := []state{{0, 0}, {0, 1}}
	for len(queue) > 0 {
		s := queue[0]
		queue = queue[1:]
		next := 1 - s.colour
		for _, m := range adj[next][s.node] {
			if dist[next][m] < 0 {
				dist[next][m] = dist[s.colour][s.node] + 1
				queue = append(queue, state{m, next})
			}
		}
	}
	answer := make([]int64, n)
	for x := int64(0); x < n; x++ {
		a, b := dist[0][x], dist[1][x]
		if a < 0 {
			answer[x] = b
		} else if b < 0 {
			answer[x] = a
		} else {
			answer[x] = min(a, b)
		}
	}
	return answer
}

var seed int64 = 1129

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func edges(n, m int64) [][]int64 {
	out := [][]int64{}
	for k := int64(0); k < m; k++ {
		a := nextRandom() % n
		b := nextRandom() % n
		out = append(out, []int64{a, b})
	}
	return out
}

func main() {
	reds := [][][]int64{}
	blues := [][][]int64{}
	for j := 0; j < 32; j++ {
		reds = append(reds, edges(100, 400))
		blues = append(blues, edges(100, 400))
	}
	var total, check int64
	for round := int64(0); round < 1000; round++ {
		for j := int64(0); j < 32; j++ {
			at := (round*7919 + j*104729) % 400
			if round%2 == 0 {
				reds[j][at][1] = (reds[j][at][1] + 1 + round%7) % 100
			} else {
				blues[j][at][1] = (blues[j][at][1] + 1 + round%7) % 100
			}
			answer := shortestAlternatingPaths(100, reds[j], blues[j])
			for _, d := range answer {
				total += d
				check = (check*31 + d + 2) % 1000000007
			}
		}
	}
	fmt.Printf("1000 rounds over 32 graphs of 100 nodes and 400 edges of each colour: lengths total %d, checksum %d\n", total, check)
}
