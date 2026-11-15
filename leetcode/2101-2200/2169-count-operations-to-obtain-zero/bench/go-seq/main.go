// LeetCode #2169: Count Operations to Obtain Zero -- the benchmark's Go
// mirror of operations.kara.
package main

import "fmt"

func countOperations(num1, num2 int64) int64 {
	a, b := max(num1, num2), min(num1, num2)
	var ops int64
	for b > 0 {
		ops += a / b
		a, b = b, a%b
	}
	return ops
}

func main() {
	var total, check int64
	for a := int64(0); a <= 3000; a++ {
		for b := int64(0); b <= 3000; b++ {
			ops := countOperations(a, b)
			total += ops
			check = (check*31 + ops) % 1000000007
		}
	}
	fmt.Printf("9006001 solves: %d in all, checksum %d\n", total, check)
}
