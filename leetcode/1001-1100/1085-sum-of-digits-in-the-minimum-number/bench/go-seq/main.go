// Benchmark: LeetCode #1085 Sum of Digits in the Minimum Number -- the ★
// arm. Mirrors ../sum_of_digits.kara, .rs, .c and .py.
package main

import "fmt"

func sumOfDigits(nums []int64) int64 {
	least := nums[0]
	for _, v := range nums {
		if v < least {
			least = v
		}
	}
	var sum int64
	for least > 0 {
		sum += least % 10
		least /= 10
	}
	if sum%2 == 0 {
		return 1
	}
	return 0
}

var seed int64 = 1085

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := int64(5000)
	arrays := make([][]int64, 2000)
	for t := range arrays {
		low := nextRandom()%100 + 1
		nums := make([]int64, 100)
		for j := range nums {
			nums[j] = low + nextRandom()%(101-low)
		}
		arrays[t] = nums
	}
	var ones, check int64
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < 2000; i++ {
			a := sumOfDigits(arrays[(r*7+i)%2000])
			ones += a
			check = (check*31 + a + i) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 2000 arrays of 100 values: %d answer 1, checksum %d\n", rounds, ones, check)
}
