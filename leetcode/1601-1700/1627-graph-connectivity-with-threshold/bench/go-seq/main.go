// LeetCode #1627: Graph Connectivity With Threshold -- the bench's Go
// mirror: the ★ arm on 100 problems of 10000 cities, thresholds 0 to 99,
// each asked the same 100000 queries, all drawn first.
package main

import "fmt"

func find(parent []int32, x int32) int32 {
	root := x
	for parent[root] != root {
		root = parent[root]
	}
	for parent[x] != root {
		next := parent[x]
		parent[x] = root
		x = next
	}
	return root
}

func areConnected(n, threshold int32, queries [][]int32) []bool {
	parent := make([]int32, n+1)
	for i := range parent {
		parent[i] = int32(i)
	}
	for z := threshold + 1; z <= n; z++ {
		for m := 2 * z; m <= n; m += z {
			a, b := find(parent, z), find(parent, m)
			if a != b {
				parent[b] = a
			}
		}
	}
	answers := make([]bool, len(queries))
	for i, q := range queries {
		answers[i] = find(parent, q[0]) == find(parent, q[1])
	}
	return answers
}

var seed int64 = 1627

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n int64 = 10000
	thresholds := make([]int32, 100)
	for i := range thresholds {
		thresholds[i] = int32(nextRandom() % 100)
	}
	queries := make([][]int32, 100000)
	for i := range queries {
		a := nextRandom()%n + 1
		b := nextRandom()%n + 1
		queries[i] = []int32{int32(a), int32(b)}
	}
	var check, total int64
	for _, threshold := range thresholds {
		var yes int64
		for _, answer := range areConnected(int32(n), threshold, queries) {
			if answer {
				yes++
			}
		}
		total += yes
		check = (check*31 + yes + 1) % 1000000007
	}
	fmt.Printf("100 problems of 10000 cities and 100000 queries: %d connected, checksum %d\n", total, check)
}
