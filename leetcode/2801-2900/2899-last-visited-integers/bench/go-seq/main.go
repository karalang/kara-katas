// LeetCode #2899: Last Visited Integers -- the bench's Go mirror (last.kara).
package main

import "fmt"

var seed int64 = 2899

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func lastVisitedIntegers(nums []int64) []int64 {
	var seen, ans []int64
	k := 0
	for _, v := range nums {
		if v == -1 {
			k++
			if k <= len(seen) {
				ans = append(ans, seen[len(seen)-k])
			} else {
				ans = append(ans, -1)
			}
		} else {
			seen = append(seen, v)
			k = 0
		}
	}
	return ans
}

func main() {
	const count, rounds, n = 10000, 20, 100
	cases := make([][]int64, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			if nextRandom()%3 == 0 {
				nums = append(nums, -1)
			} else {
				nums = append(nums, nextRandom()%100+1)
			}
		}
		cases[c] = nums
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range cases {
			ans := lastVisitedIntegers(nums)
			check = (check*31 + int64(len(ans)) + r) % 1000000007
			for _, v := range ans {
				total += v
				check = (check*31 + v + 2) % 1000000007
			}
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: answers total %d, checksum %d\n", count, n, rounds, total, check)
}
