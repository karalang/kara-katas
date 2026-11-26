// LeetCode #1782: Count Pairs Of Nodes -- the bench in Go, mirroring
// count_pairs.kara: two pointers over the sorted degrees less the joined
// pairs.
package main

import (
	"fmt"
	"sort"
)

type pair struct{ a, b int32 }

func countPairs(n int32, edges [][]int32, queries []int32) []int32 {
	degree := make([]int32, n+1)
	shared := map[pair]int32{}
	for _, e := range edges {
		a, b := e[0], e[1]
		if a > b {
			a, b = b, a
		}
		degree[a]++
		degree[b]++
		shared[pair{a, b}]++
	}
	sorted := append([]int32(nil), degree[1:]...)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i] < sorted[j] })
	answers := make([]int32, 0, len(queries))
	for _, q := range queries {
		var count int64
		lo, hi := 0, len(sorted)-1
		for lo < hi {
			if sorted[lo]+sorted[hi] > q {
				count += int64(hi - lo)
				hi--
			} else {
				lo++
			}
		}
		for p, c := range shared {
			sum := degree[p.a] + degree[p.b]
			if sum > q && sum-c <= q {
				count--
			}
		}
		answers = append(answers, int32(count))
	}
	return answers
}

var seed int64 = 1782

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	graphs := make([][][]int32, 0, 10)
	for g := int64(0); g < 10; g++ {
		span := 50 + g*2216
		edges := make([][]int32, 0, 100000)
		for e := 0; e < 100000; e++ {
			a := 1 + nextRandom()%span
			b := 1 + (a+nextRandom()%(span-1))%span
			edges = append(edges, []int32{int32(a), int32(b)})
		}
		graphs = append(graphs, edges)
	}
	var check int64
	for g := int64(0); g < 10; g++ {
		top := 400000 / (50 + g*2216)
		queries := make([]int32, 20)
		for k := int64(0); k < 20; k++ {
			queries[k] = int32((check + k*997) % top)
		}
		for _, a := range countPairs(20000, graphs[g], queries) {
			check = (check*31 + int64(a) + 1) % 1000000007
		}
	}
	fmt.Printf("10 graphs of 100000 edges: checksum %d\n", check)
}
