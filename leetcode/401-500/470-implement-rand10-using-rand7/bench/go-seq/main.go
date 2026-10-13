// Benchmark for #470: mirror of rand10.kara (the ★ arm: rejection
// sampling) on the same workload, over the same seeded rand7.
package main

import "fmt"

type rand7Source struct {
	seed int64
}

func (r *rand7Source) rand7() int64 {
	r.seed = (r.seed*1103515245 + 12345) % 2147483648
	return 1 + (r.seed/65536)%7
}

func rand10(rng *rand7Source) int64 {
	for {
		a := rng.rand7()
		v := (a-1)*7 + rng.rand7()
		if v <= 40 {
			return 1 + (v-1)%10
		}
	}
}

func main() {
	const n = 20000000
	rng := &rand7Source{seed: 470}
	var counts [11]int64
	var checksum int64
	for i := 0; i < n; i++ {
		value := rand10(rng)
		counts[value]++
		checksum = (checksum*11 + value) % 1000000007
	}
	fmt.Printf("%d draws: %d ones, %d tens, checksum %d\n", n, counts[1], counts[10], checksum)
}
