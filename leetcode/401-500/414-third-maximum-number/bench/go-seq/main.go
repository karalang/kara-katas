// LeetCode #414: Third Maximum Number -- Go mirror of third_max.kara
// (three slots).
package main

import "fmt"

func thirdMax(nums []int64) int64 {
	has1, has2, has3 := false, false, false
	var first, second, third int64
	for _, x := range nums {
		if (has1 && x == first) || (has2 && x == second) || (has3 && x == third) {
			continue
		}
		if !has1 {
			first, has1 = x, true
			continue
		}
		if x > first {
			third, has3 = second, has2
			second, has2 = first, true
			first = x
			continue
		}
		if !has2 {
			second, has2 = x, true
			continue
		}
		if x > second {
			third, has3 = second, true
			second = x
			continue
		}
		if !has3 || x > third {
			third, has3 = x, true
		}
	}
	if has3 {
		return third
	}
	return first
}

var seed int64 = 414

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func value() int64 {
	high := step()
	low := step()
	return high*131072 + low*4 - 2147483648
}

func main() {
	var n int64 = 10000
	var rounds int64 = 50000
	nums := make([]int64, 0, n)
	for i := int64(0); i < n; i++ {
		nums = append(nums, value())
	}
	var total, checksum int64
	for r := int64(0); r < rounds; r++ {
		nums[r*7919%n] = value()
		answer := thirdMax(nums)
		total += answer
		checksum = (checksum*31 + answer%1000000007 + 1000000007) % 1000000007
	}
	fmt.Printf("%d rounds on %d numbers: total %d, checksum %d\n", rounds, n, total, checksum)
}
