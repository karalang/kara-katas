// LeetCode #2359: Find Closest Node to Given Two Nodes -- the bench, the ★
// arm in Go: each start's path walked for its distances, then every node
// both reach scanned for the least of the larger distance.
package main

import "fmt"

func distances(edges []int64, start int64) []int64 {
	dist := make([]int64, len(edges))
	for i := range dist {
		dist[i] = -1
	}
	node := start
	d := int64(0)
	for node != -1 && dist[node] == -1 {
		dist[node] = d
		node = edges[node]
		d++
	}
	return dist
}

func closestMeetingNode(edges []int64, node1, node2 int64) int64 {
	d1 := distances(edges, node1)
	d2 := distances(edges, node2)
	best := int64(-1)
	bestDist := int64(-1)
	for v := range edges {
		if d1[v] >= 0 && d2[v] >= 0 {
			far := max(d1[v], d2[v])
			if best < 0 || far < bestDist {
				best = int64(v)
				bestDist = far
			}
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
	// graph a: 10^5 nodes shuffled into one line, each link cut with a
	// chance of 1 in 2^(a + 4), the last node linked back to the first
	// when a is odd; 20 random pairs of starts in each
	n := int64(100000)
	seed := int64(2359)
	graphs := make([][]int64, 0, 10)
	starts := make([][]int64, 0, 10)
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
		for i := int64(0); i < n-1; i++ {
			if nextRandom(&seed)%cut != 0 {
				edges[order[i]] = order[i+1]
			}
		}
		if a%2 == 1 {
			edges[order[n-1]] = order[0]
		}
		graphs = append(graphs, edges)
		pairs := make([]int64, 40)
		for j := range pairs {
			pairs[j] = wideRandom(&seed) % n
		}
		starts = append(starts, pairs)
	}
	check := int64(0)
	for p := int64(0); p < 10; p++ {
		for a := 0; a < 10; a++ {
			for j := 0; j < 20; j++ {
				m := closestMeetingNode(graphs[a], starts[a][2*j], starts[a][2*j+1])
				check = (check*31 + m + 2 + p) % 1000000007
			}
		}
	}
	fmt.Printf("10 passes over 10 graphs of 10^5 nodes: checksum %d\n", check)
}
