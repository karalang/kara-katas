// LeetCode #932: Beautiful Array -- bench: divide and conquer with a
// memo. Mirrors beautiful_array.kara, .c, .rs and .py.

package main

import "fmt"

func build(n int64, memo map[int64][]int64) []int64 {
	if done, ok := memo[n]; ok {
		return append([]int64(nil), done...)
	}
	out := []int64{}
	if n == 1 {
		out = append(out, 1)
	} else {
		for _, x := range build((n+1)/2, memo) {
			out = append(out, 2*x-1)
		}
		for _, x := range build(n/2, memo) {
			out = append(out, 2*x)
		}
	}
	memo[n] = append([]int64(nil), out...)
	return out
}

func beautifulArray(n int64) []int64 {
	memo := map[int64][]int64{}
	return build(n, memo)
}

func main() {
	var rounds int64 = 100
	var top int64 = 1000
	var total int64
	var check int64
	for r := int64(0); r < rounds; r++ {
		// each round builds the array for every n from 1 to top, starting
		// from a different n
		for i := int64(0); i < top; i++ {
			n := (r+i)%top + 1
			nums := beautifulArray(n)
			total += nums[n/2]
			check = (check*1000003 + nums[n-1]) % 1000000007
		}
	}
	fmt.Printf("%d rounds over n from 1 to %d: middles summing to %d, checksum %d\n", rounds, top, total, check)
}
