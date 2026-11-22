// LeetCode #2778: Sum of Squares of Special Elements -- the bench in Go:
// the ★ arm over 100000 random arrays, all drawn first, then each
// answered 20 times.
package main

import "fmt"

func sumOfSquares(nums []int64) int64 {
	n := len(nums)
	var total int64
	for i := 1; i <= n; i++ {
		if n%i == 0 {
			total += nums[i-1] * nums[i-1]
		}
	}
	return total
}

var seed int64 = 2778

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 100000
	rounds := 20
	arrays := make([][]int64, count)
	for c := 0; c < count; c++ {
		n := nextRandom()%50 + 1
		arrays[c] = make([]int64, n)
		for i := range arrays[c] {
			arrays[c][i] = nextRandom()%50 + 1
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, nums := range arrays {
			s := sumOfSquares(nums)
			total += s
			check = (check*31 + s + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays, %d rounds: sums total %d, checksum %d\n", count, rounds, total, check)
}
