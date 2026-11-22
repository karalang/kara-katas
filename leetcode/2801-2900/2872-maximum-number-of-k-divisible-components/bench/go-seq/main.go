// LeetCode #2872: Maximum Number of K-Divisible Components -- the bench,
// as components.kara: 30 trees of 3 * 10^4 nodes, each answered 20 times
// by the breadth-first arm.
package main

import "fmt"

func maxKDivisibleComponents(n int, edges [][]int64, values []int64, k int64) int64 {
	adjacent := make([][]int, n)
	for _, e := range edges {
		adjacent[e[0]] = append(adjacent[e[0]], int(e[1]))
		adjacent[e[1]] = append(adjacent[e[1]], int(e[0]))
	}
	parent := make([]int, n)
	for i := range parent {
		parent[i] = -1
	}
	order := []int{0}
	for head := 0; head < len(order); head++ {
		u := order[head]
		for _, w := range adjacent[u] {
			if w != parent[u] {
				parent[w] = u
				order = append(order, w)
			}
		}
	}
	rest := make([]int64, n)
	for i, v := range values {
		rest[i] = v % k
	}
	var parts int64
	for i := n - 1; i >= 0; i-- {
		u := order[i]
		if rest[u] == 0 {
			parts++
		} else if parent[u] >= 0 {
			rest[parent[u]] = (rest[parent[u]] + rest[u]) % k
		}
	}
	return parts
}

var seed int64 = 2872

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 30, 20, 30000
	type kase struct {
		edges  [][]int64
		values []int64
		k      int64
	}
	cases := make([]kase, count)
	for c := 0; c < count; c++ {
		k := nextRandom()%9 + 2
		edges := make([][]int64, 0, n-1)
		for v := int64(1); v < n; v++ {
			reach := v
			if c%2 == 1 && reach > 5 {
				reach = 5
			}
			edges = append(edges, []int64{v - 1 - wide()%reach, v})
		}
		values := make([]int64, n)
		var sum int64
		for i := range values {
			values[i] = wide() % 1000000001
			sum += values[i]
		}
		values[0] += (k - sum%k) % k
		cases[c] = kase{edges, values, k}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, cs := range cases {
			parts := maxKDivisibleComponents(n, cs.edges, cs.values, cs.k)
			total += parts
			check = (check*31 + parts + r) % 1000000007
		}
	}
	fmt.Printf("%d trees of %d, %d rounds: %d components, checksum %d\n", count, n, rounds, total, check)
}
