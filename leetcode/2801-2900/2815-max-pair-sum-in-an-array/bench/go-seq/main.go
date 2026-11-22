// LeetCode #2815: Max Pair Sum in an Array -- the bench in Go: the ★ arm
// over 20000 arrays of 100 numbers up to 10^4, all drawn first, then each
// answered 10 times.
package main

import "fmt"

func largestDigit(x int64) int64 {
	var top int64
	for x > 0 {
		top = max(top, x%10)
		x /= 10
	}
	return top
}

func maxSum(nums []int64) int64 {
	var best [10]int64
	answer := int64(-1)
	for _, x := range nums {
		d := largestDigit(x)
		if best[d] > 0 {
			answer = max(answer, best[d]+x)
		}
		best[d] = max(best[d], x)
	}
	return answer
}

var seed int64 = 2815

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 20000, 10
	arrays := make([][]int64, count)
	for a := range arrays {
		arrays[a] = make([]int64, 100)
		for i := range arrays[a] {
			arrays[a][i] = nextRandom()%10000 + 1
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, nums := range arrays {
			v := maxSum(nums)
			total += v
			check = (check*31 + v + 2 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 100, %d rounds: sums total %d, checksum %d\n", count, rounds, total, check)
}
