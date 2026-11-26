// LeetCode #1462 bench in Go: the ★ arm (the closure of the prerequisites
// by Floyd-Warshall) on the same 400 cases of 100 courses and 10^4
// queries.
package main

import "fmt"

func checkIfPrerequisite(n int, prerequisites [][]int32, queries [][]int32) []bool {
	before := make([][]bool, n)
	for i := range before {
		before[i] = make([]bool, n)
	}
	for _, p := range prerequisites {
		before[p[0]][p[1]] = true
	}
	for k := 0; k < n; k++ {
		for u := 0; u < n; u++ {
			if before[u][k] {
				for v := 0; v < n; v++ {
					if before[k][v] {
						before[u][v] = true
					}
				}
			}
		}
	}
	out := make([]bool, len(queries))
	for i, q := range queries {
		out[i] = before[q[0]][q[1]]
	}
	return out
}

var seed int64 = 1462

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type kase struct{ pre, qs [][]int32 }
	cases := make([]kase, 0, 400)
	for c := 0; c < 400; c++ {
		order := make([]int64, 100)
		for i := range order {
			order[i] = int64(i)
		}
		for i := int64(99); i >= 1; i-- {
			j := nextRandom() % (i + 1)
			order[i], order[j] = order[j], order[i]
		}
		var pre [][]int32
		for i := 0; i < 100; i++ {
			for j := i + 1; j < 100; j++ {
				if nextRandom()%20 == 0 {
					pre = append(pre, []int32{int32(order[i]), int32(order[j])})
				}
			}
		}
		var qs [][]int32
		for len(qs) < 10000 {
			u := nextRandom() % 100
			v := nextRandom() % 100
			if u != v {
				qs = append(qs, []int32{int32(u), int32(v)})
			}
		}
		cases = append(cases, kase{pre, qs})
	}
	var check int64
	for _, k := range cases {
		for _, a := range checkIfPrerequisite(100, k.pre, k.qs) {
			if a {
				check = (check*3 + 2) % 1000000007
			} else {
				check = (check*3 + 1) % 1000000007
			}
		}
	}
	fmt.Printf("400 cases of 100 courses and 10^4 queries: checksum %d\n", check)
}
