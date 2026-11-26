// LeetCode #1786: Number of Restricted Paths From First to Last Node -- the
// bench in Go, mirroring count_restricted_paths.kara: Dijkstra from node n
// with container/heap, then the paths summed in the order the nodes settled.
package main

import (
	"container/heap"
	"fmt"
)

type item struct {
	d int64
	u int32
}

type queue []item

func (q queue) Len() int { return len(q) }
func (q queue) Less(i, j int) bool {
	return q[i].d < q[j].d || (q[i].d == q[j].d && q[i].u < q[j].u)
}
func (q queue) Swap(i, j int)  { q[i], q[j] = q[j], q[i] }
func (q *queue) Push(x any)   { *q = append(*q, x.(item)) }
func (q *queue) Pop() any {
	old := *q
	x := old[len(old)-1]
	*q = old[:len(old)-1]
	return x
}

type arc struct {
	v int32
	w int64
}

func countRestrictedPaths(n int32, edges [][]int32) int32 {
	adj := make([][]arc, n+1)
	for _, e := range edges {
		adj[e[0]] = append(adj[e[0]], arc{e[1], int64(e[2])})
		adj[e[1]] = append(adj[e[1]], arc{e[0], int64(e[2])})
	}
	dist := make([]int64, n+1)
	for i := range dist {
		dist[i] = -1
	}
	order := make([]int32, 0, n)
	q := &queue{{0, n}}
	for q.Len() > 0 {
		it := heap.Pop(q).(item)
		if dist[it.u] != -1 {
			continue
		}
		dist[it.u] = it.d
		order = append(order, it.u)
		for _, a := range adj[it.u] {
			if dist[a.v] == -1 {
				heap.Push(q, item{it.d + a.w, a.v})
			}
		}
	}
	ways := make([]int64, n+1)
	ways[n] = 1
	for _, u := range order {
		for _, a := range adj[u] {
			if dist[a.v] < dist[u] {
				ways[u] = (ways[u] + ways[a.v]) % 1000000007
			}
		}
	}
	return int32(ways[1])
}

var seed int64 = 1786

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomGraph(n, extra int64) [][]int32 {
	edges := make([][]int32, 0, n+extra)
	joined := make(map[[2]int64]bool)
	for v := int64(2); v <= n; v++ {
		u := 1 + nextRandom()%(v-1)
		w := 1 + nextRandom()%100000
		joined[[2]int64{u, v}] = true
		edges = append(edges, []int32{int32(u), int32(v), int32(w)})
	}
	for k := int64(0); k < extra; k++ {
		a := 1 + nextRandom()%n
		b := 1 + nextRandom()%n
		u, v := a, b
		if b < a {
			u, v = b, a
		}
		if u == v || joined[[2]int64{u, v}] {
			continue
		}
		w := 1 + nextRandom()%100000
		joined[[2]int64{u, v}] = true
		edges = append(edges, []int32{int32(u), int32(v), int32(w)})
	}
	return edges
}

func main() {
	graphs := make([][][]int32, 0, 200)
	for g := 0; g < 200; g++ {
		graphs = append(graphs, randomGraph(2000, 2001))
	}
	var check int64
	for call := int64(0); call < 1000; call++ {
		edges := graphs[(check+call)%200]
		check = (check*31 + int64(countRestrictedPaths(2000, edges))) % 1000000007
	}
	fmt.Printf("1000 calls over 200 graphs: checksum %d\n", check)
}
