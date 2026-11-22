// LeetCode #2748: Number of Beautiful Pairs -- the bench (beautiful.kara
// in Go): the first digits seen so far counted, each number adding the
// counts of the digits coprime to its last digit.
package main

import "fmt"

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func countBeautifulPairs(nums []int64) int64 {
	var firsts [10]int64
	var pairs int64
	for _, x := range nums {
		last := x % 10
		for d := int64(1); d < 10; d++ {
			if gcd(d, last) == 1 {
				pairs += firsts[d]
			}
		}
		first := x
		for first >= 10 {
			first /= 10
		}
		firsts[first]++
	}
	return pairs
}

var seed int64 = 2748

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 20000, 10
	lists := make([][]int64, count)
	for k := range lists {
		nums := make([]int64, 100)
		for i := range nums {
			x := nextRandom()%9999 + 1
			if x%10 == 0 {
				x++
			}
			nums[i] = x
		}
		lists[k] = nums
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range lists {
			pairs := countBeautifulPairs(nums)
			sum += pairs
			check = (check*31 + pairs + r) % 1000000007
		}
	}
	fmt.Printf("%d lists of 100 numbers, %d rounds: pairs sum to %d, checksum %d\n", count, rounds, sum, check)
}
