// LeetCode #1615: Maximal Network Rank -- the bench in Go, mirroring
// rank.kara: each city's degree and a table of which pairs share a road,
// then every pair's rank.
package main

import "fmt"

func maximalNetworkRank(n int, roads [][2]int32) int32 {
	degree := make([]int32, n)
	joined := make([][]bool, n)
	for i := range joined {
		joined[i] = make([]bool, n)
	}
	for _, r := range roads {
		a, b := r[0], r[1]
		degree[a]++
		degree[b]++
		joined[a][b] = true
		joined[b][a] = true
	}
	var best int32
	for a := 0; a < n; a++ {
		for b := a + 1; b < n; b++ {
			rank := degree[a] + degree[b]
			if joined[a][b] {
				rank--
			}
			if rank > best {
				best = rank
			}
		}
	}
	return best
}

func main() {
	seed := int64(1615)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	const n = 100
	var networks [][][2]int32
	for k := 0; k < 2000; k++ {
		var roads [][2]int32
		for a := int32(0); a < n; a++ {
			for b := a + 1; b < n; b++ {
				if nextRandom()%4 == 0 {
					roads = append(roads, [2]int32{a, b})
				}
			}
		}
		networks = append(networks, roads)
	}
	var check, roadsSeen int64
	for _, roads := range networks {
		check = (check*31 + int64(maximalNetworkRank(n, roads)) + 1) % 1000000007
		roadsSeen += int64(len(roads))
	}
	fmt.Printf("2000 networks of 100 cities: %d roads, checksum %d\n", roadsSeen, check)
}
