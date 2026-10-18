// LeetCode 754 — Reach a Number, bench: the ★ arm (step by step),
// mirrored from reach_number.kara.
package main

import "fmt"

func reachNumber(target int64) int64 {
	t := target
	if t < 0 {
		t = -t
	}
	var k, sum int64
	for sum < t || (sum-t)%2 != 0 {
		k++
		sum += k
	}
	return k
}

var seed int64 = 754

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := int64(30000)
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		a := nextRandom()
		b := nextRandom()
		target := (a*32768+b)%1000000000 + 1
		if nextRandom()%2 == 0 {
			target = -target
		}
		moves := reachNumber(target)
		total += moves
		check = (check*31 + moves) % 1000000007
	}
	fmt.Printf("%d targets: %d moves in all, checksum %d\n", rounds, total, check)
}
