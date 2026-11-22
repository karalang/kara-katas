// LeetCode #2876: Count Visited Nodes in a Directed Graph -- the bench,
// as visited.kara: 20 graphs of 10^5 nodes, each answered 20 times by
// the peeling arm.
package main

import "fmt"

func countVisitedNodes(edges []int64) []int64 {
	n := int64(len(edges))
	incoming := make([]int64, n)
	for _, e := range edges {
		incoming[e]++
	}
	peeled := make([]int64, 0, n)
	for u := int64(0); u < n; u++ {
		if incoming[u] == 0 {
			peeled = append(peeled, u)
		}
	}
	for head := 0; head < len(peeled); head++ {
		w := edges[peeled[head]]
		incoming[w]--
		if incoming[w] == 0 {
			peeled = append(peeled, w)
		}
	}
	answer := make([]int64, n)
	for start := int64(0); start < n; start++ {
		if incoming[start] > 0 && answer[start] == 0 {
			cycle := []int64{start}
			for u := edges[start]; u != start; u = edges[u] {
				cycle = append(cycle, u)
			}
			for _, v := range cycle {
				answer[v] = int64(len(cycle))
			}
		}
	}
	for i := len(peeled) - 1; i >= 0; i-- {
		u := peeled[i]
		answer[u] = answer[edges[u]] + 1
	}
	return answer
}

var seed int64 = 2876

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 20, 20, 100000
	graphs := make([][]int64, count)
	for c := range graphs {
		edges := make([]int64, n)
		for i := int64(0); i < n; i++ {
			if c%2 == 1 {
				edges[i] = (i + nextRandom()%5 + 1) % n
			} else {
				edges[i] = (i + wide()%(n-1) + 1) % n
			}
		}
		graphs[c] = edges
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, edges := range graphs {
			counts := countVisitedNodes(edges)
			for _, v := range counts {
				total += v
			}
			check = (check*31 + counts[r] + counts[n-1-r]) % 1000000007
		}
	}
	fmt.Printf("%d graphs of %d, %d rounds: visits total %d, checksum %d\n", count, n, rounds, total, check)
}
