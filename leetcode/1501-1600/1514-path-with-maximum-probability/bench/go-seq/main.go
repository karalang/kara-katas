// LeetCode #1514: Path with Maximum Probability -- the bench: 10 graphs of
// 50000 nodes and 100000 edges built once, then 5 questions asked of each
// by the ★ arm: Dijkstra for the largest product on container/heap.
package main

import (
	"container/heap"
	"fmt"
	"math"
)

type entry struct {
	chance float64
	node   int64
}

type maxHeap []entry

func (h maxHeap) Len() int { return len(h) }
func (h maxHeap) Less(i, j int) bool {
	return h[i].chance > h[j].chance || (h[i].chance == h[j].chance && h[i].node > h[j].node)
}
func (h maxHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x interface{}) { *h = append(*h, x.(entry)) }
func (h *maxHeap) Pop() interface{} {
	old := *h
	e := old[len(old)-1]
	*h = old[:len(old)-1]
	return e
}

type edge struct{ a, b int64 }
type arc struct {
	to int64
	p  float64
}

func maxProbability(n int64, edges []edge, succProb []float64, start, end int64) float64 {
	adjacent := make([][]arc, n)
	for i, e := range edges {
		adjacent[e.a] = append(adjacent[e.a], arc{e.b, succProb[i]})
		adjacent[e.b] = append(adjacent[e.b], arc{e.a, succProb[i]})
	}
	best := make([]float64, n)
	best[start] = 1.0
	h := &maxHeap{{1.0, start}}
	for h.Len() > 0 {
		e := heap.Pop(h).(entry)
		if e.node == end {
			return e.chance
		}
		if e.chance < best[e.node] {
			continue
		}
		for _, x := range adjacent[e.node] {
			through := e.chance * x.p
			if through > best[x.to] {
				best[x.to] = through
				heap.Push(h, entry{through, x.to})
			}
		}
	}
	return 0.0
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := nextRandom(seed) * 32768
	return hi + nextRandom(seed)
}

func main() {
	seed := int64(1514)
	n := int64(50000)
	type graph struct {
		edges []edge
		probs []float64
	}
	graphs := make([]graph, 10)
	for g := range graphs {
		for i := 0; i < 100000; i++ {
			a := wide(&seed) % n
			b := (a + 1 + wide(&seed)%(n-1)) % n
			graphs[g].edges = append(graphs[g].edges, edge{a, b})
			graphs[g].probs = append(graphs[g].probs, float64(nextRandom(&seed)%21+80)/100.0)
		}
	}
	var check int64
	for r := 0; r < 5; r++ {
		for _, g := range graphs {
			start := wide(&seed) % n
			end := wide(&seed) % n
			p := maxProbability(n, g.edges, g.probs, start, end)
			check = (check*31 + int64(math.Floor(p*1000000000000.0+0.5)) + 1) % 1000000007
		}
	}
	fmt.Printf("50 questions over 10 graphs of 50000 nodes: checksum %d\n", check)
}
