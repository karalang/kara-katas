// LeetCode #2742: Painting the Walls -- the bench (walls.kara in Go): a
// knapsack over the walls covered.
package main

import (
	"fmt"
	"math"
)

func paintWalls(cost, time []int64) int64 {
	n := len(cost)
	far := int64(math.MaxInt64 / 2)
	least := make([]int64, n+1)
	for j := range least {
		least[j] = far
	}
	least[0] = 0
	for i := 0; i < n; i++ {
		for j := n; j >= 1; j-- {
			from := max(int64(j)-time[i]-1, 0)
			least[j] = min(least[j], least[from]+cost[i])
		}
	}
	return least[n]
}

var seed int64 = 2742

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n, rounds = 20, 500, 100
	costs := make([][]int64, 0, count)
	times := make([][]int64, 0, count)
	for c := 0; c < count; c++ {
		cost := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			hi := nextRandom()
			lo := nextRandom()
			cost = append(cost, (hi*32768+lo)%1000000+1)
		}
		time := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			time = append(time, nextRandom()%20+1)
		}
		costs = append(costs, cost)
		times = append(times, time)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			least := paintWalls(costs[c], times[c])
			sum += least
			check = (check*31 + least + r) % 1000000007
		}
	}
	fmt.Printf("%d cases of %d walls, %d rounds: costs sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
