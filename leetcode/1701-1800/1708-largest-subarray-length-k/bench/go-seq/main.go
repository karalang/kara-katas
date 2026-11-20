// LeetCode #1708: Largest Subarray Length K -- the Go mirror of the bench
// (largest.kara): the largest first value among the starts that leave
// room for k, on 50 random arrays of 100000 distinct values, each
// answered 100 times.
package main

import "fmt"

func largestSubarray(nums []int32, k int) []int32 {
	best := 0
	for i := 1; i <= len(nums)-k; i++ {
		if nums[i] > nums[best] {
			best = i
		}
	}
	answer := make([]int32, k)
	copy(answer, nums[best:best+k])
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 50
	var rounds int64 = 100
	var n int64 = 100000
	var seed int64 = 1708
	nums := make([][]int32, count)
	ks := make([]int, count)
	for p := 0; p < count; p++ {
		nums[p] = make([]int32, n)
		for i := int64(0); i < n; i++ {
			nums[p][i] = int32(i)
		}
		for i := n - 1; i >= 1; i-- {
			a := nextRandom(&seed)
			j := (a*32768 + nextRandom(&seed)) % (i + 1)
			nums[p][i], nums[p][j] = nums[p][j], nums[p][i]
		}
		for i := int64(0); i < n; i++ {
			nums[p][i] = nums[p][i]*10000 + int32(nextRandom(&seed)%10000)
		}
		a := nextRandom(&seed)
		ks[p] = int((a*32768+nextRandom(&seed))%n + 1)
	}
	var chosen, check int64
	for r := int64(0); r < rounds; r++ {
		for p := 0; p < count; p++ {
			answer := largestSubarray(nums[p], ks[p])
			l := int64(len(answer))
			chosen += l
			check = (check*31 + l + int64(answer[0]) + int64(answer[l-1]) + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: %d chosen, checksum %d\n", count, n, rounds, chosen, check)
}
