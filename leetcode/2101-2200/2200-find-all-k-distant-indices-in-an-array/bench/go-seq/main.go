// benchmark's Go mirror of distant.kara (LeetCode #2200, the ★ arm): the
// key's windows, a `next` index.
package main

import "fmt"

func findKDistantIndices(nums []int64, key, k int64) []int64 {
	n := int64(len(nums))
	out := []int64{}
	var next int64
	for j := int64(0); j < n; j++ {
		if nums[j] != key {
			continue
		}
		from := next
		if j-k > next {
			from = j - k
		}
		to := n - 1
		if j+k < n-1 {
			to = j + k
		}
		for i := from; i <= to; i++ {
			out = append(out, i)
		}
		next = to + 1
	}
	return out
}

var seed int64 = 2200

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type kase struct {
	nums   []int64
	key, k int64
}

func main() {
	tops := []int64{50, 200, 1000}
	cases := []kase{}
	for c := 0; c < 1000; c++ {
		nums := make([]int64, 1000)
		for i := range nums {
			nums[i] = nextRandom()%tops[c%3] + 1
		}
		key := nums[nextRandom()%1000]
		k := nextRandom()%20 + 1
		cases = append(cases, kase{nums, key, k})
	}
	var check int64
	for pass := 0; pass < 600; pass++ {
		for _, cs := range cases {
			out := findKDistantIndices(cs.nums, cs.key, cs.k)
			check = (check*31 + int64(len(out))) % 1000000007
			if len(out) > 0 {
				check = (check*31 + out[len(out)/2]) % 1000000007
			}
		}
	}
	fmt.Printf("600 passes over 1000 arrays: checksum %d\n", check)
}
