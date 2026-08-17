// Benchmark workload for LeetCode #261 — Graph Valid Tree (Go mirror).
// Mirrors valid_tree.kara algorithm-for-algorithm.
package main

import "fmt"

func find(parent []int64, x int64) int64 {
	r := x
	for parent[r] != r {
		r = parent[r]
	}
	c := x
	for parent[c] != r {
		nxt := parent[c]
		parent[c] = r
		c = nxt
	}
	return r
}

func main() {
	var n int64 = 100000
	var rounds int64 = 240
	m := n - 1

	eu := make([]int64, m)
	ev := make([]int64, m)
	var state int64 = 261261
	for i := int64(1); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		wd1 := state / 65536
		state = (state*1103515245 + 12345) & 2147483647
		eu[i-1] = (wd1 * 32768 + state / 65536) % i
		ev[i-1] = i
	}
	for sh := m - 1; sh > 0; sh-- {
		state = (state*1103515245 + 12345) & 2147483647
		wd0 := state / 65536
		state = (state*1103515245 + 12345) & 2147483647
		j := (wd0 * 32768 + state / 65536) % (sh + 1)
		eu[sh], eu[j] = eu[j], eu[sh]
		ev[sh], ev[j] = ev[j], ev[sh]
	}

	parent := make([]int64, n)
	size := make([]int64, n)

	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		for k := int64(0); k < n; k++ {
			parent[k] = k
			size[k] = 1
		}

		start := (r * 7919) % m
		components := n
		cyclic := false
		for e := int64(0); e < m; {
			idx := (start + e) % m
			ra := find(parent, eu[idx])
			rb := find(parent, ev[idx])
			if ra == rb {
				cyclic = true
				e = m
			} else {
				if size[ra] < size[rb] {
					parent[ra] = rb
					size[rb] += size[ra]
				} else {
					parent[rb] = ra
					size[ra] += size[rb]
				}
				components--
				e++
			}
		}

		var acc int64 = 0
		for p := int64(0); p < n; p++ {
			acc = (acc*31 + parent[p]) % 1000000007
		}
		var verdict int64 = 0
		if components == 1 && !cyclic {
			verdict = 1
		}
		sink = (sink*131 + acc + verdict) % 1000000007
	}

	fmt.Println(sink)
}
