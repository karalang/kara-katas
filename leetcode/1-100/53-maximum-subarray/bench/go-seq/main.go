// Bench mirror of maxsub_bench.kara — Kadane over a batch of LCG-generated arrays,
// int64 sink of per-array answers. go build. See ../../README.md § Benchmarks.
package main

import "fmt"

func main() {
	var m int64 = 1103515245       // glibc LCG multiplier
	var inc int64 = 12345          // glibc LCG increment
	var modulus int64 = 2147483648 // 2^31
	var windows int64 = 120000     // number of simulated input arrays
	var w int64 = 1000             // length of each array

	var state int64 = 1 // LCG seed
	var sink int64 = 0
	for k := int64(0); k < windows; k++ {
		state = (state*m + inc) % modulus
		v0 := (state % 100) - 50
		best := v0
		here := v0
		for j := int64(1); j < w; j++ {
			state = (state*m + inc) % modulus
			v := (state % 100) - 50
			if here+v > v {
				here = here + v
			} else {
				here = v
			}
			if here > best {
				best = here
			}
		}
		sink += best
	}
	fmt.Println(sink)
}
