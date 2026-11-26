// LeetCode #1377 bench -- Go: the ★ arm: the chance of the frog being on
// each vertex, moved one second at a time, a vertex with unvisited
// neighbours handing its chance to them in equal shares.
package main

import (
	"fmt"
	"math"
)

func frogPosition(n int, edges [][]int32, t int, target int) float64 {
	adjacent := make([][]int, n+1)
	for _, e := range edges {
		adjacent[e[0]] = append(adjacent[e[0]], int(e[1]))
		adjacent[e[1]] = append(adjacent[e[1]], int(e[0]))
	}
	seen := make([]bool, n+1)
	seen[1] = true
	chance := make([]float64, n+1)
	chance[1] = 1.0
	level := []int{1}
	for s := 0; s < t; s++ {
		var next []int
		for _, u := range level {
			var ahead []int
			for _, v := range adjacent[u] {
				if !seen[v] {
					ahead = append(ahead, v)
				}
			}
			if len(ahead) == 0 {
				continue
			}
			share := chance[u] / float64(len(ahead))
			for _, v := range ahead {
				seen[v] = true
				chance[v] = share
				next = append(next, v)
			}
			chance[u] = 0.0
		}
		level = next
	}
	return chance[target]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 50 trees of 100 vertices built once; then 100000 rounds, each asking
	// one tree, a time and a target drawn from the checksum so far for the
	// frog's chance, counted in units of 2^-20 (see the Kāra bench)
	const n = int64(100)
	seed := int64(1377)
	trees := make([][][]int32, 0, 50)
	for c := 0; c < 50; c++ {
		order := make([]int64, n)
		for i := range order {
			order[i] = int64(i) + 1
		}
		for i := n - 1; i >= 1; i-- {
			j := nextRandom(&seed) % (i + 1)
			order[i], order[j] = order[j], order[i]
		}
		edges := make([][]int32, 0, n-1)
		for k := int64(1); k < n; k++ {
			var back int64
			if c%2 == 0 {
				back = nextRandom(&seed) % k
			} else {
				back = k - 1 - nextRandom(&seed)%min(k, 3)
			}
			edges = append(edges, []int32{int32(order[k]), int32(order[back])})
		}
		trees = append(trees, edges)
	}
	check := int64(0)
	for r := int64(0); r < 100000; r++ {
		c := check % 50
		t := 1 + (check/50)%50
		target := 1 + (check/2500+r)%n
		p := frogPosition(int(n), trees[c], int(t), int(target))
		check = (check*31 + int64(math.Floor(p*1048576.0+0.5)) + r) % 1000000007
	}
	fmt.Printf("100000 rounds over 50 trees of 100 vertices: checksum %d\n", check)
}
