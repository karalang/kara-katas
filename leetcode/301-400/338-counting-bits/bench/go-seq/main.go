// Benchmark workload for LeetCode #338 — Go mirror of counting_bits.kara.
package main

import "fmt"

const (
	nN      = 1000000
	rounds  = 300
	modulus = 1073741789
)

func countBits(n int64) []int64 {
	ans := make([]int64, n+1)
	for i := int64(1); i <= n; i++ {
		ans[i] = ans[i>>1] + (i & 1)
	}
	return ans
}

func main() {
	sink := int64(0)
	for r := int64(0); r < rounds; r++ {
		n := int64(nN) - r
		ans := countBits(n)
		picked := ans[n]*10000 + ans[n/3]*100 + ans[(n*7)/11]
		sink = (sink*1000003 + picked + int64(len(ans))) % modulus
	}
	fmt.Println(sink)
}
