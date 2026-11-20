// LeetCode #1716: Calculate Money in Leetcode Bank -- the Go mirror of the
// bench (money.kara): whole weeks and the days left in closed form, on
// 500000 random n, each answered 20 times.
package main

import "fmt"

func totalMoney(n int32) int32 {
	weeks := n / 7
	days := n % 7
	return 28*weeks + 7*weeks*(weeks-1)/2 + days*(weeks+1) + days*(days-1)/2
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 500000
	var rounds int64 = 20
	var seed int64 = 1716
	ns := make([]int32, count)
	for i := range ns {
		ns[i] = int32(nextRandom(&seed)%1000 + 1)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, n := range ns {
			answer := int64(totalMoney(n))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d values of n, %d rounds: answers sum to %d, checksum %d\n", count, rounds, sum, check)
}
