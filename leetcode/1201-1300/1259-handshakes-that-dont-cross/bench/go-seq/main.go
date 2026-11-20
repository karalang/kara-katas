// LeetCode #1259 bench, in Go: the ★ arm (ways[k] for k pairs, summed over
// where person 0's partner sits, modulo 10^9 + 7) for every even count of
// people from 2 to 1000, 4 rounds; each count folded into a checksum.
package main

import "fmt"

func numberOfWays(numPeople int64) int64 {
	const m = 1000000007
	pairs := numPeople / 2
	ways := make([]int64, pairs+1)
	ways[0] = 1
	for k := int64(1); k <= pairs; k++ {
		for left := int64(0); left < k; left++ {
			ways[k] = (ways[k] + ways[left]*ways[k-1-left]) % m
		}
	}
	return ways[pairs]
}

func main() {
	check := int64(0)
	for r := 0; r < 4; r++ {
		for n := int64(2); n <= 1000; n += 2 {
			check = (check*131 + numberOfWays(n)) % 1000000007
		}
	}
	fmt.Printf("4 rounds of 2 to 1000 people: checksum %d\n", check)
}
