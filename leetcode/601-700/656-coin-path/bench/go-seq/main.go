// Benchmark for #656: cheapest cost to the end, worked backwards, as the
// Kara ★ arm.
package main

import (
	"fmt"
	"math"
)

const unreachable = math.MaxInt64

func cheapestJump(coins []int64, maxJump int64) []int64 {
	n := int64(len(coins))
	cost := make([]int64, n)
	next := make([]int64, n)
	for i := range cost {
		cost[i] = unreachable
		next[i] = -1
	}
	if coins[n-1] != -1 {
		cost[n-1] = coins[n-1]
	}
	for i := n - 2; i >= 0; i-- {
		if coins[i] == -1 {
			continue
		}
		last := i + maxJump
		if last > n-1 {
			last = n - 1
		}
		for j := i + 1; j <= last; j++ {
			if cost[j] != unreachable && coins[i]+cost[j] < cost[i] {
				cost[i] = coins[i] + cost[j]
				next[i] = j
			}
		}
	}
	path := []int64{}
	if cost[0] == unreachable {
		return path
	}
	for at := int64(0); at != -1; at = next[at] {
		path = append(path, at+1)
	}
	return path
}

var seed int64 = 656

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	inputs, rounds, n := 8, 40, 100000
	rows := make([][]int64, inputs)
	for k := range rows {
		rows[k] = make([]int64, 0, n)
		for i := 0; i < n; i++ {
			if i > 0 && nextRandom()%10 == 0 {
				rows[k] = append(rows[k], -1)
			} else {
				rows[k] = append(rows[k], nextRandom()%101)
			}
		}
	}
	var steps, checksum int64
	for r := 0; r < rounds; r++ {
		coins := rows[(r*3)%inputs]
		path := cheapestJump(coins, 100)
		var cost int64
		for _, p := range path {
			cost += coins[p-1]
			checksum = (checksum*31 + p) % 1000000007
		}
		steps += int64(len(path))
		checksum = (checksum*31 + cost) % 1000000007
	}
	fmt.Printf("%d rows of %d, %d rounds: %d steps, checksum %d\n", inputs, n, rounds, steps, checksum)
}
