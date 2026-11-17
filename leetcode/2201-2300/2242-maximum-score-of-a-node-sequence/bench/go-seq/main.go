// LeetCode #2242: Maximum Score of a Node Sequence -- the benchmark's Go
// mirror of score.kara: each node's neighbours sorted by score, largest
// first, and cut to three; every edge as the middle one tries the nine
// pairs, all four distinct.
package main

import (
	"fmt"
	"sort"
)

func maximumScore(scores []int64, edges [][2]int64) int64 {
	n := len(scores)
	best3 := make([][]int64, n)
	for _, e := range edges {
		best3[e[0]] = append(best3[e[0]], e[1])
		best3[e[1]] = append(best3[e[1]], e[0])
	}
	for i := range best3 {
		list := best3[i]
		sort.Slice(list, func(x, y int) bool { return scores[list[x]] > scores[list[y]] })
		if len(list) > 3 {
			best3[i] = list[:3]
		}
	}
	best := int64(-1)
	for _, e := range edges {
		b, c := e[0], e[1]
		for _, a := range best3[b] {
			if a == c {
				continue
			}
			for _, d := range best3[c] {
				if d != a && d != b {
					best = max(best, scores[a]+scores[b]+scores[c]+scores[d])
				}
			}
		}
	}
	return best
}

var seed int64 = 2242

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	n := int64(50000)
	check := int64(0)
	for g := 0; g < 40; g++ {
		scores := make([]int64, n)
		for i := range scores {
			scores[i] = wideRandom()%100000000 + 1
		}
		edges := make([][2]int64, n)
		for j := int64(0); j < n; j++ {
			edges[j] = [2]int64{j, (j + 1 + wideRandom()%(n/2-2)) % n}
		}
		check = (check*31 + maximumScore(scores, edges)) % 1000000007
	}
	fmt.Printf("40 graphs of 50000 nodes: checksum %d\n", check)
}
