// LeetCode 191 popcount benchmark kernel (Go mirror, go build).
package main

import "fmt"

func hammingWeight(n int64) int64 {
	var count int64 = 0
	x := n
	for x != 0 {
		x = x & (x - 1)
		count++
	}
	return count
}

func main() {
	const n int64 = 2000000
	const k int64 = 10
	nums := make([]int64, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) % 2147483648
		nums[i] = state
	}
	var sink int64 = 0
	for round := int64(0); round < k; round++ {
		for _, v := range nums {
			sink += hammingWeight(v ^ round)
		}
	}
	fmt.Println(sink)
}
