// LeetCode #2714: Find Shortest Path with K Hops -- the bench (hops.kara in
// Go): Dijkstra's search over states of a node and the hops spent, a
// `container/heap` of (distance, node, hops), smallest first.
package main

import (
	"container/heap"
	"fmt"
	"math"
)

type item struct{ dist, node, hops int64 }

type queue []item

func (q queue) Len() int { return len(q) }
func (q queue) Less(i, j int) bool {
	if q[i].dist != q[j].dist {
		return q[i].dist < q[j].dist
	}
	if q[i].node != q[j].node {
		return q[i].node < q[j].node
	}
	return q[i].hops < q[j].hops
}
func (q queue) Swap(i, j int)       { q[i], q[j] = q[j], q[i] }
func (q *queue) Push(x interface{}) { *q = append(*q, x.(item)) }
func (q *queue) Pop() interface{} {
	old := *q
	it := old[len(old)-1]
	*q = old[:len(old)-1]
	return it
}

type arc struct{ to, w int64 }

func shortestPathWithHops(n int64, edges [][]int64, s, d, k int64) int64 {
	adjacent := make([][]arc, n)
	for _, e := range edges {
		adjacent[e[0]] = append(adjacent[e[0]], arc{e[1], e[2]})
		adjacent[e[1]] = append(adjacent[e[1]], arc{e[0], e[2]})
	}
	dist := make([][]int64, n)
	for i := range dist {
		dist[i] = make([]int64, k+1)
		for j := range dist[i] {
			dist[i][j] = math.MaxInt64
		}
	}
	q := &queue{}
	dist[s][0] = 0
	heap.Push(q, item{0, s, 0})
	for q.Len() > 0 {
		it := heap.Pop(q).(item)
		here, u, hops := it.dist, it.node, it.hops
		if here > dist[u][hops] {
			continue
		}
		if u == d {
			return here
		}
		for _, a := range adjacent[u] {
			v, w := a.to, a.w
			if here+w < dist[v][hops] {
				dist[v][hops] = here + w
				heap.Push(q, item{here + w, v, hops})
			}
			if hops < k && here < dist[v][hops+1] {
				dist[v][hops+1] = here
				heap.Push(q, item{here, v, hops + 1})
			}
		}
	}
	return -1
}

var seed int64 = 2714

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

type problem struct {
	edges   [][]int64
	s, d, k int64
}

func main() {
	graphs, rounds := 50, 10
	problems := make([]problem, 0, graphs)
	for g := 0; g < graphs; g++ {
		const n int64 = 500
		joined := make(map[[2]int64]bool)
		edges := make([][]int64, 0)
		for v := int64(1); v < n; v++ {
			u := nextRandom() % v
			joined[[2]int64{u, v}] = true
			edges = append(edges, []int64{u, v, wide()%1000000 + 1})
		}
		for i := 0; i < 9501; i++ {
			a, b := nextRandom()%n, nextRandom()%n
			u, v := min(a, b), max(a, b)
			if u != v && !joined[[2]int64{u, v}] {
				joined[[2]int64{u, v}] = true
				edges = append(edges, []int64{v, u, wide()%1000000 + 1})
			}
		}
		s := nextRandom() % n
		d := (s + 1 + nextRandom()%(n-1)) % n
		k := nextRandom() % 50
		problems = append(problems, problem{edges, s, d, k})
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, p := range problems {
			length := shortestPathWithHops(500, p.edges, p.s, p.d, p.k)
			sum += length
			check = (check*31 + length + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d graphs of 500 nodes, %d rounds: lengths sum to %d, checksum %d\n", graphs, rounds, sum, check)
}
