// LeetCode #133 — Go goroutine-parallel mirror (par lane, clone_bfs).
// Same BFS clone of a 10-regular ring (N=2000) as ../go-seq/clone_bfs; the K=500
// clone reduction split across NumCPU goroutines (per-worker partial + merge).
// Hand-tuned-parallel comparator for Kāra's hand-written `par {}`.
//
// cloneGraph builds its own `visited` map per call (reentrant), so the input
// ring is shared read-only across goroutines — Go pointers are freely
// shareable, so unlike the rayon mirror (which rebuilds the graph per worker
// because Rust's Rc is not Send) no per-worker rebuild is needed. blackBox
// mirrors the seq lane's hoist guard. Sink = 500 (K × root clone val 1).
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n       = 2000
	halfDeg = 5
	k       = 500
)

type Node struct {
	val       int64
	neighbors []*Node
}

//go:noinline
func blackBox(node *Node) *Node { return node }

func cloneGraph(root *Node) *Node {
	visited := map[int64]*Node{root.val: {val: root.val}}
	queue := []*Node{root}
	for len(queue) > 0 {
		curr := queue[0]
		queue = queue[1:]
		currClone := visited[curr.val]
		for _, nb := range curr.neighbors {
			if _, ok := visited[nb.val]; !ok {
				visited[nb.val] = &Node{val: nb.val}
				queue = append(queue, nb)
			}
			currClone.neighbors = append(currClone.neighbors, visited[nb.val])
		}
	}
	return visited[root.val]
}

func main() {
	nodes := make([]*Node, n)
	for i := 0; i < n; i++ {
		nodes[i] = &Node{val: int64(i + 1)}
	}
	for i := 0; i < n; i++ {
		for d := 1; d <= halfDeg; d++ {
			j := (i + d) % n
			nodes[i].neighbors = append(nodes[i].neighbors, nodes[j])
			nodes[j].neighbors = append(nodes[j].neighbors, nodes[i])
		}
	}

	workers := runtime.NumCPU()
	if workers > k {
		workers = k
	}
	chunk := k / workers
	partials := make([]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)
	for w := 0; w < workers; w++ {
		go func(w int) {
			defer wg.Done()
			start := w * chunk
			end := start + chunk
			if w == workers-1 {
				end = k
			}
			var s int64
			for i := start; i < end; i++ {
				c := cloneGraph(blackBox(nodes[0]))
				s += c.val
			}
			partials[w] = s
		}(w)
	}
	wg.Wait()
	var sum int64
	for _, p := range partials {
		sum += p
	}
	fmt.Println(sum)
}
