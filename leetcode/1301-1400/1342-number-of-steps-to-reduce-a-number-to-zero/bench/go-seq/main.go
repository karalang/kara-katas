// LeetCode #1342 bench in Go: the ★ arm (halve an even number, take one
// from an odd one, count the steps) on the same 5 passes over 10^6 + 1
// numbers.
package main

import "fmt"

func numberOfSteps(num int32) int32 {
	var steps int32
	for num > 0 {
		if num%2 == 0 {
			num /= 2
		} else {
			num--
		}
		steps++
	}
	return steps
}

func main() {
	var check int64
	for pass := int64(0); pass < 5; pass++ {
		for x := int64(0); x < 1000001; x++ {
			steps := numberOfSteps(int32((x + check) % 1000001))
			check = (check*31 + int64(steps) + pass) % 1000000007
		}
	}
	fmt.Printf("5 passes over 10^6 + 1 numbers: checksum %d\n", check)
}
