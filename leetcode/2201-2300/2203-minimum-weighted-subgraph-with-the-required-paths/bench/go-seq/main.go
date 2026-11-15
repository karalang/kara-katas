// benchmark's Go mirror of subgraph.kara (LeetCode #2203, the ★ arm): three
// Dijkstras with a binary heap of (distance, node) pairs, the last over the
// edges turned round, and the least sum over the meeting node.
package main

import "fmt"

type arc struct{ to, w int64 }

type item struct{ d, u int64 }

func less(x, y item) bool { return x.d < y.d || (x.d == y.d && x.u < y.u) }

type heap []item

func (q *heap) push(it item) {
	*q = append(*q, it)
	h := *q
	i := len(h) - 1
	for i > 0 {
		p := (i - 1) / 2
		if !less(it, h[p]) {
			break
		}
		h[i] = h[p]
		i = p
	}
	h[i] = it
}

func (q *heap) pop() item {
	h := *q
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
	*q = h
	return top
}

func dijkstra(adj [][]arc, from int64) []int64 {
	dist := make([]int64, len(adj))
	for i := range dist {
		dist[i] = -1
	}
	q := heap{}
	q.push(item{0, from})
	for len(q) > 0 {
		it := q.pop()
		if dist[it.u] >= 0 {
			continue
		}
		dist[it.u] = it.d
		for _, a := range adj[it.u] {
			if dist[a.to] < 0 {
				q.push(item{it.d + a.w, a.to})
			}
		}
	}
	return dist
}

func minimumWeight(n int64, edges [][3]int64, src1, src2, dest int64) int64 {
	forward := make([][]arc, n)
	backward := make([][]arc, n)
	for _, e := range edges {
		forward[e[0]] = append(forward[e[0]], arc{e[1], e[2]})
		backward[e[1]] = append(backward[e[1]], arc{e[0], e[2]})
	}
	one := dijkstra(forward, src1)
	two := dijkstra(forward, src2)
	home := dijkstra(backward, dest)
	best := int64(-1)
	for v := int64(0); v < n; v++ {
		if one[v] >= 0 && two[v] >= 0 && home[v] >= 0 {
			total := one[v] + two[v] + home[v]
			if best < 0 || total < best {
				best = total
			}
		}
	}
	return best
}

var seed int64 = 2203

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func main() {
	const n = 20000
	graphs := [][][3]int64{}
	for g := 0; g < 4; g++ {
		edges := [][3]int64{}
		for len(edges) < 60000 {
			from := wideRandom() % n
			to := wideRandom() % n
			if from != to {
				edges = append(edges, [3]int64{from, to, wideRandom()%100000 + 1})
			}
		}
		graphs = append(graphs, edges)
	}
	var check int64
	for pass := 0; pass < 5; pass++ {
		for _, edges := range graphs {
			for t := int64(0); t < 4; t++ {
				weight := minimumWeight(n, edges, t*3, t*3+1, t*3+2)
				check = (check*31 + weight + 1) % 1000000007
			}
		}
	}
	fmt.Printf("5 passes over 4 graphs: checksum %d\n", check)
}
