// LeetCode #1192 bench: the ★ arm in Go, over the same 4 networks and 10
// rounds as the Kāra bench.
package main

import "fmt"

type arc struct{ v, id int }

type frame struct{ u, via, next int }

func criticalConnections(n int, connections [][]int) [][]int {
	adj := make([][]arc, n)
	for id, c := range connections {
		adj[c[0]] = append(adj[c[0]], arc{c[1], id})
		adj[c[1]] = append(adj[c[1]], arc{c[0], id})
	}
	disc := make([]int, n)
	low := make([]int, n)
	for i := range disc {
		disc[i] = -1
	}
	var bridges [][]int
	disc[0] = 0
	time := 1
	stack := []frame{{0, -1, 0}}
	for len(stack) > 0 {
		top := len(stack) - 1
		f := stack[top]
		u := f.u
		if f.next < len(adj[u]) {
			stack[top].next++
			a := adj[u][f.next]
			if a.id == f.via {
				continue
			}
			if disc[a.v] == -1 {
				disc[a.v] = time
				low[a.v] = time
				time++
				stack = append(stack, frame{a.v, a.id, 0})
			} else {
				low[u] = min(low[u], disc[a.v])
			}
		} else {
			stack = stack[:top]
			if top > 0 {
				p := stack[top-1].u
				low[p] = min(low[p], low[u])
				if low[u] > disc[p] {
					bridges = append(bridges, []int{p, u})
				}
			}
		}
	}
	return bridges
}

var seed int64 = 1192

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type pair struct{ a, b int64 }

func randomNetwork(n, extra int64) [][]int {
	joined := map[pair]bool{}
	var edges [][]int
	for v := int64(1); v < n; v++ {
		u := nextRandom() % v
		joined[pair{u, v}] = true
		edges = append(edges, []int{int(u), int(v)})
	}
	for k := int64(0); k < extra; k++ {
		a := nextRandom() % n
		b := nextRandom() % n
		key := pair{min(a, b), max(a, b)}
		if a != b && !joined[key] {
			joined[key] = true
			edges = append(edges, []int{int(a), int(b)})
		}
	}
	return edges
}

func main() {
	path := make([][]int, 0, 99999)
	for i := 0; i < 99999; i++ {
		path = append(path, []int{i, i + 1})
	}
	ring := append(append([][]int{}, path...), []int{99999, 0})
	type network struct {
		n     int
		edges [][]int
	}
	networks := []network{
		{50000, randomNetwork(50000, 50001)},
		{100000, randomNetwork(100000, 0)},
		{100000, path},
		{100000, ring},
	}
	var check int64
	for r := 0; r < 10; r++ {
		for _, nw := range networks {
			bridges := criticalConnections(nw.n, nw.edges)
			check = (check*131 + int64(len(bridges))) % 1000000007
			for _, b := range bridges {
				check = (check*131 + int64(b[0])*100003 + int64(b[1])) % 1000000007
			}
		}
	}
	fmt.Printf("10 rounds of 4 networks of up to 100000 servers: checksum %d\n", check)
}
