// Benchmark for #779: K-th Symbol in Grammar -- mirror of the ★ arm (the
// ones in k - 1), with the same workload as the Kāra program.
package main

import (
	"fmt"
	"math/bits"
)

func kthGrammar(n, k int64) int64 {
	_ = n
	return int64(bits.OnesCount64(uint64(k-1)) % 2)
}

func main() {
	var x, ones int64 = 779, 0
	for i := 0; i < 200000000; i++ {
		k := 1 + x%536870912
		answer := kthGrammar(30, k)
		ones += answer
		x = (x*1103515245 + 12345 + answer) % 2147483648
	}
	fmt.Printf("200000000 queries of row 30: %d ones, last state %d\n", ones, x)
}
