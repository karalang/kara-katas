// LeetCode #2165: Smallest Value of the Rearranged Number -- the
// benchmark's Go mirror of smallest.kara.
package main

import (
	"fmt"
	"sort"
	"strconv"
)

func smallestNumber(num int64) int64 {
	size := num
	if size < 0 {
		size = -size
	}
	text := strconv.FormatInt(size, 10)
	digits := make([]int64, 0, len(text))
	for _, c := range text {
		digits = append(digits, int64(c-'0'))
	}
	if num < 0 {
		sort.Slice(digits, func(i, j int) bool { return digits[i] > digits[j] })
	} else {
		sort.Slice(digits, func(i, j int) bool { return digits[i] < digits[j] })
		for i, d := range digits {
			if d != 0 {
				digits[0], digits[i] = digits[i], digits[0]
				break
			}
		}
	}
	var out int64
	for _, d := range digits {
		out = out*10 + d
	}
	if num < 0 {
		return -out
	}
	return out
}

var seed int64 = 2165

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	nums := make([]int64, 1000)
	for k := range nums {
		length := nextRandom()%14 + 1
		var num int64
		for i := int64(0); i < length; i++ {
			num = num*10 + nextRandom()%10
		}
		if nextRandom()%2 == 1 {
			num = -num
		}
		nums[k] = num
	}
	var check int64
	for r := 0; r < 1000; r++ {
		for k := range nums {
			nums[k] = nums[k] + nextRandom()%2001 - 1000
			s := smallestNumber(nums[k])
			check = (check*31 + s%1000000007 + 1000000007) % 1000000007
		}
	}
	fmt.Printf("1000000 solves: checksum %d\n", check)
}
