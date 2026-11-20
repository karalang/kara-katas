// LeetCode #1230 bench: the ★ arm in Go, over the same 200 sets of 1000
// coins as the Kāra bench.
package main

import "fmt"

func probabilityOfHeads(prob []float64, target int) float64 {
	ways := make([]float64, target+1)
	ways[0] = 1.0
	for _, p := range prob {
		for j := target; j >= 1; j-- {
			ways[j] = ways[j]*(1.0-p) + ways[j-1]*p
		}
		ways[0] = ways[0] * (1.0 - p)
	}
	return ways[target]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1230)
	sets := make([][]float64, 200)
	targets := make([]int, 200)
	for s := 0; s < 200; s++ {
		sets[s] = make([]float64, 1000)
		for i := range sets[s] {
			sets[s][i] = float64(nextRandom(&seed)%1001) / 1000.0
		}
		targets[s] = int(nextRandom(&seed) % 1001)
	}
	total := 0.0
	for s := 0; s < 200; s++ {
		total += probabilityOfHeads(sets[s], targets[s])
	}
	fmt.Printf("200 sets of 1000 coins: total %.6f\n", total)
}
