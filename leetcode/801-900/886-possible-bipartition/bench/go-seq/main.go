// LeetCode #886 bench: Go mirror of possible_bipartition.kara (the ★ arm,
// two colours by breadth-first search) on the same 4000 groups.
package main

import (
	"fmt"
	"slices"
)

func possibleBipartition(n int64, dislikes [][]int64) bool {
	adj := make([][]int64, n+1)
	for _, d := range dislikes {
		adj[d[0]] = append(adj[d[0]], d[1])
		adj[d[1]] = append(adj[d[1]], d[0])
	}
	colour := make([]int64, n+1)
	for i := range colour {
		colour[i] = -1
	}
	queue := []int64{}
	for start := int64(1); start <= n; start++ {
		if colour[start] >= 0 {
			continue
		}
		colour[start] = 0
		queue = append(queue[:0], start)
		for len(queue) > 0 {
			u := queue[0]
			queue = queue[1:]
			for _, v := range adj[u] {
				if colour[v] < 0 {
					colour[v] = 1 - colour[u]
					queue = append(queue, v)
				} else if colour[v] == colour[u] {
					return false
				}
			}
		}
	}
	return true
}

var seed int64 = 886

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var yes, check int64
	for g := 0; g < 4000; g++ {
		// n people, each disliking the people five distinct offsets on,
		// every offset below n / 2 so that no pair repeats: 5n pairs, up
		// to 10^4; the offsets odd, but one of them even half the time
		n := 1000 + nextRandom()%1001
		spoil := nextRandom()%2 == 0
		offsets := []int64{}
		for len(offsets) < 5 {
			d := 1 + nextRandom()%(n/2-1)
			if d%2 == 0 && !(spoil && len(offsets) == 0) {
				d--
			}
			if !slices.Contains(offsets, d) {
				offsets = append(offsets, d)
			}
		}
		dislikes := [][]int64{}
		for a := int64(0); a < n; a++ {
			for k := 0; k < 5; k++ {
				dislikes = append(dislikes, []int64{a + 1, (a+offsets[k])%n + 1})
			}
		}
		var bit int64
		if possibleBipartition(n, dislikes) {
			bit = 1
		}
		yes += bit
		check = (check*3 + bit + 1) % 1000000007
	}
	fmt.Printf("4000 groups of up to 2000 people: %d can be split, checksum %d\n", yes, check)
}
