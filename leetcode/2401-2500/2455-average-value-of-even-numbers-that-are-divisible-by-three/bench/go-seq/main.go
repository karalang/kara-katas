// LeetCode #2455: Average Value of Even Numbers That Are Divisible by
// Three -- bench, Go mirror of average.kara: one pass sums and counts the
// values divisible by 6.
package main

import "fmt"

func averageValue(nums []int64) int64 {
	var sum, count int64
	for _, x := range nums {
		if x%6 == 0 {
			sum += x
			count++
		}
	}
	if count == 0 {
		return 0
	}
	return sum / count
}

var seed int64 = 2455

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 1000)
	for a := range arrays {
		nums := make([]int64, 1000)
		for i := range nums {
			nums[i] = 1 + nextRandom()%1000
		}
		arrays[a] = nums
	}
	var check int64
	for p := int64(0); p < 250; p++ {
		for a := int64(0); a < 1000; a++ {
			arrays[a][(p*7919+a)%1000] = 1 + check%1000
			check = (check*31 + averageValue(arrays[a]) + p) % 1000000007
		}
	}
	fmt.Printf("250 passes over 1000 arrays of 1000 values: checksum %d\n", check)
}
