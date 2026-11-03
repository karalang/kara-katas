// Benchmark lane for LeetCode 1040 -- Go mirror of moving_stones.kara.
package main

import (
	"fmt"
	"slices"
)

func moves(stones []int64) (int64, int64) {
	s := append([]int64(nil), stones...)
	slices.Sort(s)
	n := int64(len(s))
	most := s[n-1] - s[1] - n + 2
	if b := s[n-2] - s[0] - n + 2; b > most {
		most = b
	}
	least := n
	i := int64(0)
	for j := int64(0); j < n; j++ {
		for s[j]-s[i] >= n {
			i++
		}
		inside := j - i + 1
		cost := n - inside
		if inside == n-1 && s[j]-s[i] == n-2 {
			cost = 2
		}
		if cost < least {
			least = cost
		}
	}
	return least, most
}

var seed int64 = 1040

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func draw(top int64) int64 {
	a := nextRandom()
	b := nextRandom()
	return (a*32768 + b) % top
}

func main() {
	const count, size, rounds = 400, 10000, 5
	sets := make([][]int64, 0, count)
	for c := 0; c < count; c++ {
		widest := int64(3)
		if c%2 == 0 {
			widest = 100000
		}
		stones := make([]int64, 0, size)
		at := int64(0)
		for k := 0; k < size; k++ {
			at += draw(widest) + 1
			stones = append(stones, at)
		}
		for i := int64(size - 1); i > 0; i-- {
			j := draw(i + 1)
			stones[i], stones[j] = stones[j], stones[i]
		}
		sets = append(sets, stones)
	}
	total, check := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for _, stones := range sets {
			least, most := moves(stones)
			total += least + most
			check = (check*131 + least*1000003 + most) % 1000000007
		}
	}
	fmt.Printf("%d sets of %d stones, %d rounds: total %d, checksum %d\n", count, size, rounds, total, check)
}
