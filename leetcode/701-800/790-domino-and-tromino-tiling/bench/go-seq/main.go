// LeetCode 790 — Domino and Tromino Tiling: the bench, in Go.
// Mirrors num_tilings.kara: two growing tables of counts, full and
// ragged ends, for 300,000 random n.
package main

import "fmt"

func numTilings(n int64) int64 {
	const modulus = 1000000007
	full := []int64{1, 1}
	ragged := []int64{0, 1}
	for i := int64(2); i <= n; i++ {
		full = append(full, (full[i-1]+full[i-2]+2*ragged[i-2])%modulus)
		ragged = append(ragged, (ragged[i-1]+full[i-1])%modulus)
	}
	return full[n]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(790)
	rounds := int64(300000)
	sum, check := int64(0), int64(0)
	for r := int64(0); r < rounds; r++ {
		n := 1 + nextRandom(&seed)%1000
		ways := numTilings(n)
		sum = (sum + ways) % 1000000007
		check = (check*31 + ways) % 1000000007
	}
	fmt.Printf("%d rounds of n up to 1000: answers sum to %d, checksum %d\n", rounds, sum, check)
}
