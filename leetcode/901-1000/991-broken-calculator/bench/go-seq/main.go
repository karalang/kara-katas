// LeetCode #991: Broken Calculator -- bench, the ★ arm (greedy from the
// target back), the same algorithm and workload as broken_calc.kara.
package main

import "fmt"

func brokenCalc(startValue, target int64) int64 {
	var ops int64
	t := target
	for t > startValue {
		if t%2 == 1 {
			t++
		} else {
			t /= 2
		}
		ops++
	}
	return ops + startValue - t
}

var seed int64 = 991

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 5000
	starts := make([]int64, 1000)
	targets := make([]int64, 1000)
	for i := 0; i < 1000; i++ {
		a := nextRandom()
		starts[i] = 1 + (a*32768+nextRandom())%1000
		b := nextRandom()
		targets[i] = 1 + (b*32768+nextRandom())%1000000000
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 1000; i++ {
			got := brokenCalc(starts[(r+i)%1000], targets[i])
			total += got
			check = (check*31 + got + 1) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 1000 pairs: %d operations, checksum %d\n", rounds, total, check)
}
