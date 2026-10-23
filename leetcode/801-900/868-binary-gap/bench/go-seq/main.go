// LeetCode #868: Binary Gap -- Go mirror of the bench program (the ★ arm,
// one pass over the bits).
package main

import "fmt"

func binaryGap(n int64) int64 {
	var best int64
	last := int64(-1)
	rest := n
	var position int64
	for rest > 0 {
		if rest%2 == 1 {
			if last >= 0 && position-last > best {
				best = position - last
			}
			last = position
		}
		rest /= 2
		position++
	}
	return best
}

func main() {
	limit := int64(10000000)
	var total, check int64
	for n := int64(1); n <= limit; n++ {
		g := binaryGap(n)
		total += g
		check = (check*31 + g) % 1000000007
	}
	fmt.Printf("n from 1 to %d: gaps sum to %d, checksum %d\n", limit, total, check)
}
