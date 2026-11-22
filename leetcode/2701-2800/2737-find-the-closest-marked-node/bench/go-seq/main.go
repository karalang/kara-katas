// LeetCode #2737: Find the Closest Marked Node -- the bench (closest.kara
// in Go): Dijkstra from s with container/heap, stopping at the first
// marked node taken off it.
package main

import (
	"container/heap"
	"fmt"
	"math"
	"slices"
)

type entry struct{ d, u int64 }
type queue []entry

func (q queue) Len() int { return len(q) }
func (q queue) Less(i, j int) bool {
	return q[i].d < q[j].d || (q[i].d == q[j].d && q[i].u < q[j].u)
}
func (q queue) Swap(i, j int) { q[i], q[j] = q[j], q[i] }
func (q *queue) Push(x any)   { *q = append(*q, x.(entry)) }
func (q *queue) Pop() any {
	old := *q
	e := old[len(old)-1]
	*q = old[:len(old)-1]
	return e
}

type arc struct{ v, w int64 }

func minimumDistance(n int64, edges [][]int64, s int64, marked []int64) int64 {
	out := make([][]arc, n)
	for _, e := range edges {
		out[e[0]] = append(out[e[0]], arc{e[1], e[2]})
	}
	isMarked := make([]bool, n)
	for _, v := range marked {
		isMarked[v] = true
	}
	dist := make([]int64, n)
	for i := range dist {
		dist[i] = math.MaxInt64
	}
	q := &queue{}
	dist[s] = 0
	heap.Push(q, entry{0, s})
	for q.Len() > 0 {
		e := heap.Pop(q).(entry)
		if e.d > dist[e.u] {
			continue
		}
		if isMarked[e.u] {
			return e.d
		}
		for _, a := range out[e.u] {
			if e.d+a.w < dist[a.v] {
				dist[a.v] = e.d + a.w
				heap.Push(q, entry{e.d + a.w, a.v})
			}
		}
	}
	return -1
}

var seed int64 = 2737

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type problem struct {
	edges  [][]int64
	s      int64
	marked []int64
}

func main() {
	const graphs, n, m, rounds = 50, 500, 10000, 20
	problems := []problem{}
	for g := 0; g < graphs; g++ {
		edges := make([][]int64, 0, m)
		for i := 0; i < m; i++ {
			u := nextRandom() % n
			v := (u + 1 + nextRandom()%(n-1)) % n
			hi := nextRandom()
			w := (hi*32768+nextRandom())%1000000 + 1
			edges = append(edges, []int64{u, v, w})
		}
		s := nextRandom() % n
		marked := []int64{}
		want := int(nextRandom()%3 + 1)
		for len(marked) < want {
			v := nextRandom() % n
			if v != s && !slices.Contains(marked, v) {
				marked = append(marked, v)
			}
		}
		problems = append(problems, problem{edges, s, marked})
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range problems {
			distance := minimumDistance(n, p.edges, p.s, p.marked)
			sum += distance
			check = (check*31 + distance + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d graphs of %d nodes and %d edges, %d rounds: distances sum to %d, checksum %d\n", graphs, n, m, rounds, sum, check)
}
