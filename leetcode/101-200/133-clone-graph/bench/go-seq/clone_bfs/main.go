// LeetCode 133 — BFS clone of a 10-regular ring, Go single-threaded mirror.
// Algorithmic peer of bench/clone_bfs.{kara,rs,c,py}. Stdout sink: 500.
package main

import "fmt"

type Node struct {
	val       int64
	neighbors []*Node
}

//go:noinline
func blackBox(n *Node) *Node { return n }

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
	const N = 2000
	const halfDeg = 5
	const K = 500

	nodes := make([]*Node, N)
	for i := 0; i < N; i++ {
		nodes[i] = &Node{val: int64(i + 1)}
	}
	for i := 0; i < N; i++ {
		for d := 1; d <= halfDeg; d++ {
			j := (i + d) % N
			nodes[i].neighbors = append(nodes[i].neighbors, nodes[j])
			nodes[j].neighbors = append(nodes[j].neighbors, nodes[i])
		}
	}

	var sum int64
	for k := 0; k < K; k++ {
		c := cloneGraph(blackBox(nodes[0]))
		sum += c.val
	}
	fmt.Println(sum)
}
