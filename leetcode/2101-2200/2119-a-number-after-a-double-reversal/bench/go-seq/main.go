// LeetCode #2119: A Number After a Double Reversal -- the benchmark, the
// same algorithm as reversed.kara: each number's digits reversed by % 10
// and / 10, twice.

package main

import "fmt"

func reverse(num int64) int64 {
	n, out := num, int64(0)
	for n > 0 {
		out = out*10 + n%10
		n /= 10
	}
	return out
}

func isSameAfterReversals(num int64) bool {
	return reverse(reverse(num)) == num
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2119)
	nums := make([]int64, 0, 1000000)
	for i := 0; i < 1000000; i++ {
		num := nextRandom(&seed) % 1000001
		if nextRandom(&seed)%3 == 0 {
			num = num / 1000 * 1000
		}
		nums = append(nums, num)
	}
	var same, check int64
	for round := 0; round < 100; round++ {
		nums[round*7919%1000000]++
		for _, num := range nums {
			if isSameAfterReversals(num) {
				same++
				check = (check*31 + num%1000) % 1000000007
			}
		}
	}
	fmt.Printf("100000000 checks: %d the same, checksum %d\n", same, check)
}
