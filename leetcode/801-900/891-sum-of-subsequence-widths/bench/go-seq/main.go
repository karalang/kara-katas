// LeetCode #891 bench: Go mirror of sum_subseq_widths.kara (the counting
// arm, a count of each value) on the same 400 arrays.
package main

import "fmt"

const modulus = 1000000007

func sumSubseqWidths(nums []int64) int64 {
	n := int64(len(nums))
	var largest int64
	for _, x := range nums {
		largest = max(largest, x)
	}
	count := make([]int64, largest+1)
	for _, x := range nums {
		count[x]++
	}
	pow := make([]int64, n+1)
	pow[0] = 1
	for i := int64(1); i <= n; i++ {
		pow[i] = pow[i-1] * 2 % modulus
	}
	var total, p int64
	for v := int64(0); v <= largest; v++ {
		c := count[v]
		if c > 0 {
			block := pow[c] - 1
			asMax := pow[p] * block % modulus
			asMin := pow[n-p-c] * block % modulus
			total = (total + v*(asMax-asMin)) % modulus
			p += c
		}
	}
	return (total + modulus) % modulus
}

var seed int64 = 891

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var sum, check int64
	for c := 0; c < 400; c++ {
		nums := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			nums = append(nums, 1+nextRandom()%100000)
		}
		got := sumSubseqWidths(nums)
		sum = (sum + got) % modulus
		check = (check*131 + got) % modulus
	}
	fmt.Printf("400 arrays of 100000 numbers: widths sum to %d, checksum %d\n", sum, check)
}
