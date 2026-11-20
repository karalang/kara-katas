// LeetCode #1269 bench, in Go: the ★ arm (the ways to stand on each of
// the first `steps / 2 + 1` cells, a new row per step) on 1000 random cases
// of 1 to 500 steps in 1 to 400 cells or a million, drawn once, 20 rounds;
// every answer folded into a checksum.
package main

import "fmt"

const mod = 1000000007

func numWays(steps, arrLen int64) int64 {
	width := min(arrLen, steps/2+1)
	ways := make([]int64, width)
	ways[0] = 1
	for s := int64(0); s < steps; s++ {
		next := make([]int64, width)
		for i := int64(0); i < width; i++ {
			w := ways[i]
			if i > 0 {
				w += ways[i-1]
			}
			if i+1 < width {
				w += ways[i+1]
			}
			next[i] = w % mod
		}
		ways = next
	}
	return ways[0]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1269)
	steps := make([]int64, 1000)
	lens := make([]int64, 1000)
	for c := range steps {
		steps[c] = nextRandom(&seed)%500 + 1
		if c%4 == 0 {
			lens[c] = 1000000
		} else {
			lens[c] = nextRandom(&seed)%400 + 1
		}
	}
	var check int64
	for round := int64(0); round < 20; round++ {
		for c := range steps {
			check = (check*131 + numWays(steps[c], lens[c]) + round) % 1000000007
		}
	}
	fmt.Printf("20 rounds of 1000 cases: checksum %d\n", check)
}
