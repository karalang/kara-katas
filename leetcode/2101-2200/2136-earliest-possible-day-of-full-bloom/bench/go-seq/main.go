// LeetCode #2136: Earliest Possible Day of Full Bloom -- the benchmark,
// the same algorithm as bloom.kara.
package main

import (
	"fmt"
	"sort"
)

func earliestFullBloom(plantTime, growTime []int64, order []int) int64 {
	for i := range order {
		order[i] = i
	}
	sort.Slice(order, func(a, b int) bool { return growTime[order[a]] > growTime[order[b]] })
	planted, bloom := int64(0), int64(0)
	for _, i := range order {
		planted += plantTime[i]
		if planted+growTime[i] > bloom {
			bloom = planted + growTime[i]
		}
	}
	return bloom
}

var seed int64 = 2136

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	plants := make([][]int64, 10)
	grows := make([][]int64, 10)
	for g := 0; g < 10; g++ {
		plants[g] = make([]int64, n)
		grows[g] = make([]int64, n)
		for i := 0; i < n; i++ {
			plants[g][i] = nextRandom()%10000 + 1
			grows[g][i] = nextRandom()%10000 + 1
		}
	}
	order := make([]int, n)
	total, check := int64(0), int64(0)
	for round := int64(0); round < 10; round++ {
		for g := 0; g < 10; g++ {
			hi := nextRandom()
			at := (hi*32768 + nextRandom()) % n
			plants[g][at] = nextRandom()%10000 + 1
			grows[g][at] = nextRandom()%10000 + 1
			day := earliestFullBloom(plants[g], grows[g], order)
			total += day
			check = (check*31 + day + round) % 1000000007
		}
	}
	fmt.Printf("100 solves: %d days in all, checksum %d\n", total, check)
}
