// LeetCode #2867: Count Valid Paths in a Tree -- the bench, as
// paths.kara: 10 trees of 10^5 nodes, each answered 10 times by the
// disjoint-set arm.
package main

import "fmt"

func find(parent []int64, x int64) int64 {
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

func countPaths(n int64, edges [][]int64) int64 {
	prime := make([]bool, n+1)
	for i := int64(2); i <= n; i++ {
		prime[i] = true
	}
	for i := int64(2); i*i <= n; i++ {
		if prime[i] {
			for j := i * i; j <= n; j += i {
				prime[j] = false
			}
		}
	}
	parent := make([]int64, n+1)
	size := make([]int64, n+1)
	for i := range parent {
		parent[i] = int64(i)
		size[i] = 1
	}
	around := make([][]int64, n+1)
	for _, e := range edges {
		a, b := e[0], e[1]
		if prime[a] || prime[b] {
			around[a] = append(around[a], b)
			around[b] = append(around[b], a)
		} else {
			ra, rb := find(parent, a), find(parent, b)
			if ra != rb {
				parent[ra] = rb
				size[rb] += size[ra]
			}
		}
	}
	var count int64
	for p := int64(2); p <= n; p++ {
		if prime[p] {
			var before int64
			for _, v := range around[p] {
				if !prime[v] {
					s := size[find(parent, v)]
					count += s + s*before
					before += s
				}
			}
		}
	}
	return count
}

var seed int64 = 2867

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 10, 10, 100000
	trees := make([][][]int64, count)
	for c := 0; c < count; c++ {
		for v := int64(2); v <= n; v++ {
			reach := v - 1
			if c%2 == 1 && reach > 5 {
				reach = 5
			}
			trees[c] = append(trees[c], []int64{v - 1 - wide()%reach, v})
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, edges := range trees {
			paths := countPaths(n, edges)
			total += paths
			check = (check*31 + paths%1000000007 + r) % 1000000007
		}
	}
	fmt.Printf("%d trees of %d, %d rounds: %d paths, checksum %d\n", count, n, rounds, total, check)
}
