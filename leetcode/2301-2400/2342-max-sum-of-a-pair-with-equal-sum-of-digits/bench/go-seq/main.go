// LeetCode #2342: Max Sum of a Pair With Equal Sum of Digits -- the bench,
// the ★ arm in Go: a table of 82 keeping the largest value seen for each
// digit sum, each value paired with the largest before it of its own sum.
package main

import "fmt"

func digitSum(x int64) int64 {
	s := int64(0)
	for x > 0 {
		s += x % 10
		x /= 10
	}
	return s
}

func maximumSum(nums []int64) int64 {
	best := make([]int64, 82)
	for i := range best {
		best[i] = -1
	}
	answer := int64(-1)
	for _, x := range nums {
		s := digitSum(x)
		if best[s] >= 0 && best[s]+x > answer {
			answer = best[s] + x
		}
		if x > best[s] {
			best[s] = x
		}
	}
	return answer
}

func scrambled(index int64) int64 {
	return index * 2654435761 % 2147483647
}

func main() {
	arrays := make([][]int64, 10)
	for a := int64(0); a < 10; a++ {
		arrays[a] = make([]int64, 100000)
		for i := int64(0); i < 100000; i++ {
			arrays[a][i] = scrambled(a*100000+i)%1000000000 + 1
		}
	}
	check := int64(0)
	for p := int64(0); p < 20; p++ {
		for _, nums := range arrays {
			check = (check*31 + maximumSum(nums) + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
