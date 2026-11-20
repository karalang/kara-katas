// LeetCode #2360: Longest Cycle in a Graph -- the bench, the ★ arm in Go:
// each node stamped with the time it is first visited, and a walk that
// reaches a node stamped since it began has closed a cycle as long as the
// time between the two visits.
package main

import "fmt"

func longestCycle(edges []int64) int64 {
	n := len(edges)
	stamp := make([]int64, n)
	for i := range stamp {
		stamp[i] = -1
	}
	time := int64(0)
	best := int64(-1)
	for start := 0; start < n; start++ {
		began := time
		node := int64(start)
		for node != -1 && stamp[node] == -1 {
			stamp[node] = time
			time++
			node = edges[node]
		}
		if node != -1 && stamp[node] >= began {
			best = max(best, time-stamp[node])
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wideRandom(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func main() {
	// graph a: 10^5 nodes shuffled into one line, cut into pieces with a
	// chance of 1 in 2^(a + 4) at each link; each piece's last node points
	// back to its first with a chance of 1 in 2, and otherwise at a random
	// node
	n := int64(100000)
	seed := int64(2360)
	graphs := make([][]int64, 0, 10)
	for a := int64(0); a < 10; a++ {
		order := make([]int64, n)
		for i := range order {
			order[i] = int64(i)
		}
		for i := n - 1; i >= 1; i-- {
			j := wideRandom(&seed) % (i + 1)
			order[i], order[j] = order[j], order[i]
		}
		cut := int64(1) << (a + 4)
		edges := make([]int64, n)
		for i := range edges {
			edges[i] = -1
		}
		first := int64(0)
		for i := int64(0); i < n; i++ {
			if i == n-1 || nextRandom(&seed)%cut == 0 {
				var target int64
				if nextRandom(&seed)%2 == 0 {
					target = order[first]
				} else {
					target = wideRandom(&seed) % n
				}
				if target != order[i] {
					edges[order[i]] = target
				}
				first = i + 1
			} else {
				edges[order[i]] = order[i+1]
			}
		}
		graphs = append(graphs, edges)
	}
	check := int64(0)
	for p := int64(0); p < 50; p++ {
		for _, edges := range graphs {
			check = (check*31 + longestCycle(edges) + 2 + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 10 graphs of 10^5 nodes: checksum %d\n", check)
}
