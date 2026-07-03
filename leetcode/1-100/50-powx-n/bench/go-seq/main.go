// Bench mirror of powbench.kara — recursive fast-power, f64-bits sum sink.
// go build. See ../../README.md § Benchmarks.
package main

import (
	"fmt"
	"math"
)

func fastPow(x float64, n int64) float64 {
	if n == 0 {
		return 1.0
	}
	half := fastPow(x, n/2)
	if n%2 == 0 {
		return half * half
	}
	return half * half * x
}

func myPow(x float64, n int64) float64 {
	if n < 0 {
		return 1.0 / fastPow(x, -n)
	}
	return fastPow(x, n)
}

func main() {
	var nIters, kReps int64 = 400000, 20
	inv2048 := 0.00048828125 // 2^-11, exact
	var acc uint64 = 0
	for rep := int64(0); rep < kReps; rep++ {
		for i := int64(0); i < nIters; i++ {
			h := ((i + rep*7919) * 2654435761) & 2047
			x := 1.0 + float64(h)*inv2048
			n := ((i + rep) % 129) - 64
			acc += math.Float64bits(myPow(x, n))
		}
	}
	fmt.Println(acc & 0x7FFFFFFFFFFFFFFF)
}
