// Benchmark for #823: Binary Trees With Factors -- the ★ arm (counts in a map).
//
// Mirrors num_factored_binary_trees.kara: sort a copy of the values, so
// that both factors of a value come before it, and count each value's
// trees from its factors' counts, looked up by value in a map.
package main

import (
	"fmt"
	"sort"
)

func numFactoredBinaryTrees(arr []int64) int64 {
	const modulus = 1000000007
	values := append([]int64(nil), arr...)
	sort.Slice(values, func(a, b int) bool { return values[a] < values[b] })
	trees := make(map[int64]int64)
	var total int64
	for i, x := range values {
		count := int64(1)
		for j := 0; j < i; j++ {
			left := values[j]
			if x%left == 0 {
				if right, ok := trees[x/left]; ok {
					count = (count + trees[left]*right) % modulus
				}
			}
		}
		trees[x] = count
		total = (total + count) % modulus
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const limit = 1000000000
	smooth := []int64{}
	for p2 := int64(1); p2 <= limit; p2 *= 2 {
		for p3 := p2; p3 <= limit; p3 *= 3 {
			for p5 := p3; p5 <= limit; p5 *= 5 {
				for p7 := p5; p7 <= limit; p7 *= 7 {
					if p7 > 1 {
						smooth = append(smooth, p7)
					}
				}
			}
		}
	}
	sort.Slice(smooth, func(a, b int) bool { return smooth[a] < smooth[b] })
	count := 64
	rounds := 1000
	seed := int64(823)
	sets := make([][]int64, 0, count)
	for g := 0; g < count; g++ {
		taken := make([]bool, len(smooth))
		set := make([]int64, 0, 1000)
		for len(set) < 1000 {
			k := nextRandom(&seed) % int64(len(smooth))
			if !taken[k] {
				taken[k] = true
				set = append(set, smooth[k])
			}
		}
		sets = append(sets, set)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		answer := numFactoredBinaryTrees(sets[round%count])
		total += answer
		checksum = (checksum*131 + answer) % 1000000007
	}
	fmt.Printf("%d values, %d rounds of %d sets: total %d, checksum %d\n", len(smooth), rounds, count, total, checksum)
}
