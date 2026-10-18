// LeetCode 743 — Network Delay Time, bench: the ★ arm (Dijkstra with a
// priority queue) on a 100-node graph of 6000 edges, every source, while
// edge times change. Mirrors network_delay_time.kara.
package main

import "fmt"

type edge struct{ v, w int64 }
type entry struct{ d, u int64 }
type timeEdge struct{ u, v, w int64 }

func less(a, b entry) bool { return a.d < b.d || (a.d == b.d && a.u < b.u) }

func push(h []entry, e entry) []entry {
	h = append(h, e)
	i := len(h) - 1
	for i > 0 {
		p := (i - 1) / 2
		if !less(e, h[p]) {
			break
		}
		h[i] = h[p]
		i = p
	}
	h[i] = e
	return h
}

func pop(h []entry) ([]entry, entry) {
	top := h[0]
	last := h[len(h)-1]
	h = h[:len(h)-1]
	i := 0
	for {
		c := 2*i + 1
		if c >= len(h) {
			break
		}
		if c+1 < len(h) && less(h[c+1], h[c]) {
			c++
		}
		if !less(h[c], last) {
			break
		}
		h[i] = h[c]
		i = c
	}
	if len(h) > 0 {
		h[i] = last
	}
	return h, top
}

func networkDelayTime(times []timeEdge, n, k int64) int64 {
	adj := make([][]edge, n+1)
	for _, t := range times {
		adj[t.u] = append(adj[t.u], edge{t.v, t.w})
	}
	heard := make([]int64, n+1)
	for i := range heard {
		heard[i] = -1
	}
	queue := push(nil, entry{0, k})
	var settled, last int64
	for len(queue) > 0 {
		var e entry
		queue, e = pop(queue)
		d, u := e.d, e.u
		if heard[u] != -1 {
			continue
		}
		heard[u] = d
		settled++
		last = d
		for _, a := range adj[u] {
			if heard[a.v] == -1 {
				queue = push(queue, entry{d + a.w, a.v})
			}
		}
	}
	if settled == n {
		return last
	}
	return -1
}

var seed int64 = 743

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomGraph(n, m, maxW int64) []timeEdge {
	used := make([]bool, (n+1)*(n+1))
	var times []timeEdge
	for int64(len(times)) < m {
		u := 1 + nextRandom()%n
		v := 1 + nextRandom()%n
		if u == v || used[u*(n+1)+v] {
			continue
		}
		used[u*(n+1)+v] = true
		w := nextRandom() % (maxW + 1)
		times = append(times, timeEdge{u, v, w})
	}
	return times
}

func main() {
	rounds := 12
	times := randomGraph(100, 6000, 100)
	var total int64
	for r := 0; r < rounds; r++ {
		for c := 0; c < 50; c++ {
			i := nextRandom() % int64(len(times))
			w := nextRandom() % 101
			times[i].w = w
		}
		for k := int64(1); k <= 100; k++ {
			total += networkDelayTime(times, 100, k)
		}
	}
	fmt.Printf("%d rounds of 100 queries on 100 nodes and 6000 edges: answers sum to %d\n", rounds, total)
}
