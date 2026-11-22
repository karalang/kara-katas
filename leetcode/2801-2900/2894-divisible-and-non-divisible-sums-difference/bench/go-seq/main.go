// LeetCode #2894: Divisible and Non-divisible Sums Difference -- the
// bench, as sums.kara: every n and m from 1 to 1000, 100 rounds, by the
// formula arm.
package main

import "fmt"

func differenceOfSums(n, m int64) int64 {
	k := n / m
	return n*(n+1)/2 - m*k*(k+1)
}

func main() {
	const rounds, top = 100, 1000
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for n := int64(1); n <= top; n++ {
			for m := int64(1); m <= top; m++ {
				d := differenceOfSums(n, (m+r)%top+1)
				total += d
				check = (check*31 + d + 1000000) % 1000000007
			}
		}
	}
	fmt.Printf("%d by %d pairs, %d rounds: differences total %d, checksum %d\n", top, top, rounds, total, check)
}
