// Benchmark workload — Gray Code (LeetCode #89).
// Go mirror of ../gray_code.kara. Folds each gray code i ^ (i >> 1) through a rolling
// polynomial hash (loop-carried, iter-mixed so nothing hoists), N=65536, K=2500.
package main

import "fmt"

func main() {
	const n = 65536
	const total = 2500
	const modulus = 1000000007
	var sum int64 = 0
	for iter := int64(0); iter < total; iter++ {
		acc := iter
		for i := int64(0); i < n; i++ {
			g := i ^ (i >> 1)
			acc = (acc*131 + (g ^ iter)) % modulus
		}
		sum = (sum*131 + acc) % modulus
	}
	fmt.Println(sum)
}
