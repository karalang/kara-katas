// LeetCode #1334 bench, Go mirror of the Kāra bench: the ★ arm on 10 maps
// of 100 cities built once, then 30 passes, each setting one road's weight
// of every map and the threshold from the checksum so far, answering every
// map.
package main

import "fmt"

func findTheCity(n int, edges [][]int32, distanceThreshold int32) int {
	const far int64 = 1000000000
	dist := make([][]int64, n)
	for i := range dist {
		dist[i] = make([]int64, n)
		for j := range dist[i] {
			dist[i][j] = far
		}
		dist[i][i] = 0
	}
	for _, e := range edges {
		dist[e[0]][e[1]] = int64(e[2])
		dist[e[1]][e[0]] = int64(e[2])
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
	best := 0
	fewest := n + 1
	for i := 0; i < n; i++ {
		near := 0
		for j := 0; j < n; j++ {
			if j != i && dist[i][j] <= int64(distanceThreshold) {
				near++
			}
		}
		if near <= fewest {
			fewest = near
			best = i
		}
	}
	return best
}

var seed int64 = 1334

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100
	maps := make([][][]int32, 10)
	for t := range maps {
		edges := [][]int32{}
		for a := 0; a < n; a++ {
			for b := a + 1; b < n; b++ {
				if nextRandom()%2 == 0 {
					edges = append(edges, []int32{int32(a), int32(b), int32(1 + nextRandom()%10000)})
				}
			}
		}
		maps[t] = edges
	}
	var check int64
	for pass := int64(0); pass < 30; pass++ {
		threshold := int32(200 + check%800)
		for t := 0; t < 10; t++ {
			at := check % int64(len(maps[t]))
			maps[t][at][2] = int32(1 + check/3%10000)
			city := findTheCity(n, maps[t], threshold)
			check = (check*31 + int64(city) + pass) % 1000000007
		}
	}
	fmt.Printf("30 passes over 10 maps of 100 cities: checksum %d\n", check)
}
