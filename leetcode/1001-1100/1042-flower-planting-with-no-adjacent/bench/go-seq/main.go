// LeetCode #1042: Flower Planting With No Adjacent -- bench, Go mirror of
// garden_no_adj.kara (greedy over the gardens in order).
package main

import "fmt"

func gardenNoAdj(n int64, paths [][2]int64) []int64 {
	neighbors := make([][]int64, 0)
	for i := int64(0); i < n; i++ {
		neighbors = append(neighbors, nil)
	}
	for _, p := range paths {
		x, y := p[0], p[1]
		neighbors[x-1] = append(neighbors[x-1], y-1)
		neighbors[y-1] = append(neighbors[y-1], x-1)
	}
	answer := make([]int64, n)
	for garden := int64(0); garden < n; garden++ {
		var taken [5]bool
		for _, other := range neighbors[garden] {
			taken[answer[other]] = true
		}
		flower := int64(1)
		for taken[flower] {
			flower++
		}
		answer[garden] = flower
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomPaths(n, tries int64, seed *int64) [][2]int64 {
	joined := make([][]int64, n)
	paths := make([][2]int64, 0)
	for t := int64(0); t < tries; t++ {
		x := nextRandom(seed) % n
		y := nextRandom(seed) % n
		if x == y || len(joined[x]) >= 3 || len(joined[y]) >= 3 {
			continue
		}
		seen := false
		for _, z := range joined[x] {
			if z == y {
				seen = true
			}
		}
		if seen {
			continue
		}
		joined[x] = append(joined[x], y)
		joined[y] = append(joined[y], x)
		paths = append(paths, [2]int64{x + 1, y + 1})
	}
	return paths
}

func main() {
	const count, n, rounds = 10, int64(10000), 100
	seed := int64(1042)
	gardens := make([][][2]int64, 0)
	for g := 0; g < count; g++ {
		gardens = append(gardens, randomPaths(n, 4*n, &seed))
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, paths := range gardens {
			answer := gardenNoAdj(n, paths)
			var sum int64
			for _, flower := range answer {
				sum += flower
			}
			total += sum
			check = (check*131 + sum) % 1000000007
		}
	}
	fmt.Printf("%d gardens of %d plots, %d rounds: types sum to %d, checksum %d\n", count, n, rounds, total, check)
}
