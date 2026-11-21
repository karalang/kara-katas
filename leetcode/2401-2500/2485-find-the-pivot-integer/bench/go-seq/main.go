// LeetCode #2485: Find the Pivot Integer -- bench, Go mirror of
// pivot.kara.
package main

import (
	"fmt"
	"math"
)

func pivotInteger(n int64) int64 {
	total := n * (n + 1) / 2
	x := int64(math.Round(math.Sqrt(float64(total))))
	if x*x == total {
		return x
	}
	return -1
}

func main() {
	check := int64(0)
	for p := int64(0); p < 24000; p++ {
		start := check % 1000
		for i := int64(0); i < 1000; i++ {
			n := 1 + (start+i)%1000
			check = (check*31 + pivotInteger(n) + 2 + p) % 1000000007
		}
	}
	fmt.Printf("24000 passes over every count from 1 to 1000: checksum %d\n", check)
}
