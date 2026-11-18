// LeetCode #1617: Count Subtrees With Max Distance Between Cities -- the
// bench in Go, mirroring subtrees.kara: all pair distances by
// Floyd-Warshall, then every mask of two or more cities that holds one
// road fewer than it has cities, its largest distance counted.
package main

import (
	"fmt"
	"math/bits"
)

func countSubgraphsForEachDiameter(n int, edges [][2]int32) []int32 {
	far := int64(n + 1)
	dist := make([][]int64, n)
	for i := range dist {
		dist[i] = make([]int64, n)
		for j := range dist[i] {
			if i != j {
				dist[i][j] = far
			}
		}
	}
	ends := make([][2]int, 0, n-1)
	for _, e := range edges {
		a, b := int(e[0]-1), int(e[1]-1)
		dist[a][b], dist[b][a] = 1, 1
		ends = append(ends, [2]int{a, b})
	}
	for k := 0; k < n; k++ {
		for i := 0; i < n; i++ {
			for j := 0; j < n; j++ {
				if dist[i][k]+dist[k][j] < dist[i][j] {
					dist[i][j] = dist[i][k] + dist[k][j]
				}
			}
		}
	}
	answer := make([]int32, n-1)
	for mask := int64(1); mask < int64(1)<<n; mask++ {
		size := bits.OnesCount64(uint64(mask))
		if size < 2 {
			continue
		}
		roads := 0
		for _, e := range ends {
			if mask>>e[0]&1 == 1 && mask>>e[1]&1 == 1 {
				roads++
			}
		}
		if roads != size-1 {
			continue
		}
		var widest int64
		for i := 0; i < n; i++ {
			if mask>>i&1 == 1 {
				for j := i + 1; j < n; j++ {
					if mask>>j&1 == 1 && dist[i][j] > widest {
						widest = dist[i][j]
					}
				}
			}
		}
		answer[widest-1]++
	}
	return answer
}

var seed int64 = 1617

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

func randomTree(n int) [][2]int32 {
	name := make([]int32, n)
	for c := range name {
		name[c] = int32(c + 1)
	}
	for i := n - 1; i >= 1; i-- {
		j := nextRandom() % int64(i+1)
		name[i], name[j] = name[j], name[i]
	}
	edges := make([][2]int32, 0, n-1)
	for c := 1; c < n; c++ {
		p := nextRandom() % int64(c)
		edges = append(edges, [2]int32{name[c], name[p]})
	}
	return edges
}

func main() {
	trees := make([][][2]int32, 400)
	for t := range trees {
		trees[t] = randomTree(15)
	}
	var check, subtrees int64
	for _, edges := range trees {
		for _, x := range countSubgraphsForEachDiameter(15, edges) {
			check = mix(check, int64(x))
			subtrees += int64(x)
		}
	}
	fmt.Printf("400 trees of 15 cities: %d subtrees, checksum %d\n", subtrees, check)
}
