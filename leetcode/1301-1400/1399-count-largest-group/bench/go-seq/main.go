// LeetCode #1399 bench -- Go: each number's digit sum by peeling off its
// last digit, the groups' sizes in an array indexed by the sum, and the
// groups of the largest size counted.
package main

import "fmt"

func digitSum(x int32) int64 {
	rest := x
	sum := int64(0)
	for rest > 0 {
		sum += int64(rest % 10)
		rest /= 10
	}
	return sum
}

func countLargestGroup(n int32) int32 {
	size := make([]int32, 37)
	for x := int32(1); x <= n; x++ {
		size[digitSum(x)]++
	}
	largest := int32(0)
	for _, s := range size {
		if s > largest {
			largest = s
		}
	}
	count := int32(0)
	for _, s := range size {
		if s == largest {
			count++
		}
	}
	return count
}

func main() {
	check := int64(0)
	for r := int64(0); r < 6000; r++ {
		n := 1 + (check+r*7919)%10000
		check = (check*131 + int64(countLargestGroup(int32(n)))) % 1000000007
	}
	fmt.Printf("6000 rounds of n up to 10^4: checksum %d\n", check)
}
