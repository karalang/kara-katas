// LeetCode #2520: Count the Digits That Divide a Number -- Go mirror of the
// benchmark (digits.kara): the same numbers, passes, order and checksum.
package main

import "fmt"

func countDigits(num int64) int64 {
	rest, count := num, int64(0)
	for rest > 0 {
		if num%(rest%10) == 0 {
			count++
		}
		rest /= 10
	}
	return count
}

var seed int64 = 2520

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	nums := make([]int64, 100000)
	for t := range nums {
		length := nextRandom()%9 + 1
		var num int64
		for j := int64(0); j < length; j++ {
			num = num*10 + nextRandom()%9 + 1
		}
		nums[t] = num
	}
	const passes = 150
	var check int64
	for p := int64(0); p < passes; p++ {
		start := check % 100000
		for i := int64(0); i < 100000; i++ {
			check = (check*31 + countDigits(nums[(start+i)%100000]) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 100000 numbers: checksum %d\n", passes, check)
}
