// LeetCode #1548: The Most Similar Path in a Graph -- bench: the ★ arm (a
// DP over the target's places) over 100 connected graphs of 50 to 100
// cities named from up to 26 names, each with a target of 100 names, built
// once, each asked 20 times. Go mirror of most_similar.kara.
package main

import (
	"fmt"
	"math"
)

type road struct{ a, b int64 }

func mostSimilar(n int64, roads []road, names []string, target []string) []int64 {
	nextTo := make([][]int64, n)
	for _, r := range roads {
		nextTo[r.a] = append(nextTo[r.a], r.b)
		nextTo[r.b] = append(nextTo[r.b], r.a)
	}
	length := len(target)
	cost := make([][]int64, length)
	from := make([][]int64, length)
	for t := range cost {
		cost[t] = make([]int64, n)
		from[t] = make([]int64, n)
		for v := range cost[t] {
			cost[t][v] = math.MaxInt64
		}
	}
	for v := int64(0); v < n; v++ {
		if names[v] == target[0] {
			cost[0][v] = 0
		} else {
			cost[0][v] = 1
		}
	}
	for t := 1; t < length; t++ {
		for v := int64(0); v < n; v++ {
			miss := int64(1)
			if names[v] == target[t] {
				miss = 0
			}
			for _, u := range nextTo[v] {
				if cost[t-1][u]+miss < cost[t][v] {
					cost[t][v] = cost[t-1][u] + miss
					from[t][v] = u
				}
			}
		}
	}
	last := int64(0)
	for v := int64(1); v < n; v++ {
		if cost[length-1][v] < cost[length-1][last] {
			last = v
		}
	}
	path := make([]int64, length)
	path[length-1] = last
	for t := length - 1; t >= 1; t-- {
		path[t-1] = from[t][path[t]]
	}
	return path
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func nameOf(i int64) string {
	letters := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	name := []byte{}
	for _, place := range []int64{676, 26, 1} {
		name = append(name, letters[i/place%26])
	}
	return string(name)
}

type graph struct {
	n      int64
	roads  []road
	names  []string
	target []string
}

func main() {
	seed := int64(1548)
	graphs := []graph{}
	for g := 0; g < 100; g++ {
		n := nextRandom(&seed)%51 + 50
		own := nextRandom(&seed)%26 + 1
		names := make([]string, n)
		for v := range names {
			names[v] = nameOf(nextRandom(&seed) % own)
		}
		joined := make([][]bool, n)
		for v := range joined {
			joined[v] = make([]bool, n)
		}
		roads := []road{}
		for v := int64(1); v < n; v++ {
			u := nextRandom(&seed) % v
			joined[u][v] = true
			joined[v][u] = true
			roads = append(roads, road{v, u})
		}
		extra := nextRandom(&seed) % (4 * n)
		for k := int64(0); k < extra; k++ {
			a := nextRandom(&seed) % n
			b := nextRandom(&seed) % n
			if a != b && !joined[a][b] {
				joined[a][b] = true
				joined[b][a] = true
				roads = append(roads, road{a, b})
			}
		}
		target := make([]string, 100)
		for t := range target {
			target[t] = nameOf(nextRandom(&seed) % (own + 1))
		}
		graphs = append(graphs, graph{n, roads, names, target})
	}
	check, total := int64(0), int64(0)
	for pass := 0; pass < 20; pass++ {
		for _, g := range graphs {
			path := mostSimilar(g.n, g.roads, g.names, g.target)
			distance := int64(0)
			for t, v := range path {
				check = mix(check, v)
				if g.names[v] != g.target[t] {
					distance++
				}
			}
			total += distance
		}
	}
	fmt.Printf("20 passes over 100 graphs of up to 100 cities: distance %d, checksum %d\n", total, check)
}
