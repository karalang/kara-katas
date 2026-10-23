// LeetCode #905: Sort Array By Parity -- bench program, Go.
//
// The two pointers from both ends, over 1,000,000 numbers below 5001 built
// once. Each round sorts a copy by parity, folds the evens in front and
// one number of the answer into a checksum and changes one number.
package main

import "fmt"

func sortArrayByParity(nums []int64) []int64 {
	out := nums
	i, j := 0, len(out)-1
	for i < j {
		if out[i]%2 == 0 {
			i++
		} else if out[j]%2 == 1 {
			j--
		} else {
			out[i], out[j] = out[j], out[i]
			i++
			j--
		}
	}
	return out
}

var seed int64 = 905

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 1000000
	var rounds int64 = 100
	nums := make([]int64, n)
	for k := int64(0); k < n; k++ {
		nums[k] = nextRandom() % 5001
	}
	var check, total int64
	for round := int64(0); round < rounds; round++ {
		cp := make([]int64, n)
		copy(cp, nums)
		out := sortArrayByParity(cp)
		var lead int64
		for out[lead]%2 == 0 {
			lead++
		}
		total += lead
		check = (check*31 + lead) % 1000000007
		check = (check*31 + out[round*7919%n]) % 1000000007
		nums[round*7919%n] = nextRandom() % 5001
	}
	fmt.Printf("%d rounds over %d numbers: %d evens in front, checksum %d\n", rounds, n, total, check)
}
