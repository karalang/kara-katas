// LeetCode #646: Maximum Length of Pair Chain -- Go mirror of the Kāra
// bench.
//
// The ★ arm's greedy over the same inputs and rounds: the pair slice
// copied and sorted by right end, then every pair kept that starts after
// the last one kept ended.
package main

import (
	"fmt"
	"sort"
)

func findLongestChain(pairs [][]int64) int64 {
	order := append([][]int64(nil), pairs...)
	sort.Slice(order, func(a, b int) bool { return order[a][1] < order[b][1] })
	var count, end int64
	for _, p := range order {
		if count == 0 || p[0] > end {
			count++
			end = p[1]
		}
	}
	return count
}

var seed int64 = 646

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const inputs = 20
	const rounds = 200
	all := make([][][]int64, 0, inputs)
	for i := 0; i < inputs; i++ {
		longest := 10 + nextRandom()%991
		pairs := make([][]int64, 0, 10000)
		for j := 0; j < 10000; j++ {
			left := nextRandom() % 30000
			right := left + 1 + nextRandom()%longest
			pairs = append(pairs, []int64{left, right})
		}
		all = append(all, pairs)
	}
	var sum, checksum int64
	for r := 0; r < rounds; r++ {
		c := findLongestChain(all[(r*7)%inputs])
		sum += c
		checksum = (checksum*31 + c) % 1000000007
	}
	fmt.Printf("%d inputs, %d rounds: total %d, checksum %d\n", inputs, rounds, sum, checksum)
}
