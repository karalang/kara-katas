// LeetCode #2787: Ways to Express an Integer as Sum of Powers -- the bench
// in Go: the ★ arm over every n from 1 to 300 with every x from 1 to 5,
// 20 times over.
package main

import "fmt"

func ipow(b, e int64) int64 {
	r := int64(1)
	for ; e > 0; e-- {
		r *= b
	}
	return r
}

func numberOfWays(n, x int64) int64 {
	const modulus = 1000000007
	ways := make([]int64, n+1)
	ways[0] = 1
	for i := int64(1); ipow(i, x) <= n; i++ {
		p := ipow(i, x)
		for s := n; s >= p; s-- {
			ways[s] = (ways[s] + ways[s-p]) % modulus
		}
	}
	return ways[n]
}

func main() {
	rounds := 20
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for n := int64(1); n <= 300; n++ {
			for x := int64(1); x <= 5; x++ {
				w := numberOfWays(n, x)
				total += w
				check = (check*31 + w + r) % 1000000007
			}
		}
	}
	fmt.Printf("1500 pairs, %d rounds: ways sum to %d, checksum %d\n", rounds, total, check)
}
