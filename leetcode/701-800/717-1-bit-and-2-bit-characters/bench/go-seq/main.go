// LeetCode #717: 1-bit and 2-bit Characters -- read from the start.
// Benchmark mirror of the Kara star arm: step past one bit on a 0 and
// two on a 1; the last character is one bit when a step lands on the
// last bit.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func isOneBitCharacter(bits []int64) bool {
	n := int64(len(bits))
	i := int64(0)
	for i < n-1 {
		i += bits[i] + 1
	}
	return i == n-1
}

func main() {
	seed := int64(717)
	var strings [][]int64
	for s := int64(0); s < 100; s++ {
		density := 1 + s%3
		bits := make([]int64, 0, 10000)
		for i := 0; i < 9999; i++ {
			if nextRandom(&seed)%4 < density {
				bits = append(bits, 1)
			} else {
				bits = append(bits, 0)
			}
		}
		bits = append(bits, 0)
		strings = append(strings, bits)
	}
	yes := 0
	for round := 0; round < 400; round++ {
		for _, bits := range strings {
			at := (round * 997) % 9999
			bits[at] = 1 - bits[at]
		}
		for _, bits := range strings {
			if isOneBitCharacter(bits) {
				yes++
			}
		}
	}
	fmt.Printf("400 rounds of 100 strings of 10000 bits: %d one-bit endings\n", yes)
}
