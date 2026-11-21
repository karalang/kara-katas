// LeetCode #2453: Destroy Sequential Targets -- bench, Go mirror of
// targets.kara: a map counts each residue class, and a second pass keeps
// the least value of a largest class.
package main

import "fmt"

func destroyTargets(nums []int64, space int64) int64 {
	count := map[int64]int64{}
	for _, x := range nums {
		count[x%space]++
	}
	var best, answer int64
	for _, x := range nums {
		c := count[x%space]
		if c > best || (c == best && x < answer) {
			best = c
			answer = x
		}
	}
	return answer
}

var seed int64 = 2453

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n int64 = 100000
	arrays := make([][]int64, 10)
	for a := range arrays {
		nums := make([]int64, n)
		for i := range nums {
			hi := nextRandom()
			nums[i] = 1 + (hi*32768+nextRandom())%1000000000
		}
		arrays[a] = nums
	}
	var check int64
	for p := int64(0); p < 50; p++ {
		for a := int64(0); a < 10; a++ {
			arrays[a][(p*7919+a)%n] = 1 + check%1000000000
			space := 1 + (p*7919+a*104729)%100000
			check = (check*31 + destroyTargets(arrays[a], space) + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
