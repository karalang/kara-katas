// Benchmark for #403: mirror of frog_jump.kara (the jump sizes that reach
// each stone).
package main

import "fmt"

func canCross(stones []int64) bool {
	jumps := make(map[int64]map[int64]bool, len(stones))
	for _, s := range stones {
		jumps[s] = make(map[int64]bool)
	}
	jumps[stones[0]][0] = true
	for _, s := range stones {
		sizes := make([]int64, 0, len(jumps[s]))
		for k := range jumps[s] {
			sizes = append(sizes, k)
		}
		for _, k := range sizes {
			for size := k - 1; size < k+2; size++ {
				if size > 0 {
					if set, ok := jumps[s+size]; ok {
						set[size] = true
					}
				}
			}
		}
	}
	return len(jumps[stones[len(stones)-1]]) > 0
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	rivers := 600
	n := 2000
	var seed int64 = 403
	crossed := 0
	var checksum int64
	for r := 0; r < rivers; r++ {
		stones := []int64{0, 1}
		for len(stones) < n {
			last := stones[len(stones)-1]
			stones = append(stones, last+1+step(&seed)%3)
		}
		if canCross(stones) {
			crossed++
			checksum = (checksum*31 + int64(r) + 1) % 1000000007
		}
	}
	fmt.Printf("%d rivers of %d stones: %d crossed, checksum %d\n", rivers, n, crossed, checksum)
}
