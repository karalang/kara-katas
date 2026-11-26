// LeetCode #1486: XOR Operation in an Array -- bench, the Go twin of
// xor_operation.kara.
package main

import "fmt"

func xorOperation(n int32, start int32) int32 {
	var x int32
	for i := int32(0); i < n; i++ {
		x ^= start + 2*i
	}
	return x
}

func main() {
	var check int64
	for q := int64(0); q < 2000000; q++ {
		n := int32(1 + (check+q)%1000)
		start := int32((check/7 + q*13) % 1001)
		check = (check*31 + int64(xorOperation(n, start))) % 1000000007
	}
	fmt.Printf("2000000 calls: checksum %d\n", check)
}
