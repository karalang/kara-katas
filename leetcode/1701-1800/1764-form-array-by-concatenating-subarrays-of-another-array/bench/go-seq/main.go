// LeetCode #1764: Form Array by Concatenating Subarrays of Another Array --
// the bench in Go, mirroring can_choose.kara: greedy, each group matched at
// the first place it fits, compared value by value.
package main

import "fmt"

func canChoose(groups [][]int32, nums []int32) bool {
	at := 0
	for _, group := range groups {
		n := len(group)
		for {
			if at+n > len(nums) {
				return false
			}
			same := true
			for i := 0; i < n; i++ {
				if nums[at+i] != group[i] {
					same = false
					break
				}
			}
			if same {
				break
			}
			at++
		}
		at += n
	}
	return true
}

var seed int64 = 1764

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomValues(n, values int64) []int32 {
	v := make([]int32, n)
	for i := range v {
		v[i] = int32(nextRandom() % values)
	}
	return v
}

type kase struct {
	groups [][]int32
	nums   []int32
}

func randomCase(k, most, values, gap int64, breakOne bool) kase {
	var c kase
	for j := int64(0); j < k; j++ {
		filler := nextRandom() % (gap + 1)
		c.nums = append(c.nums, randomValues(filler, values)...)
		n := 1 + nextRandom()%most
		g := randomValues(n, values)
		c.nums = append(c.nums, g...)
		c.groups = append(c.groups, g)
	}
	if breakOne {
		g := nextRandom() % k
		at := nextRandom() % int64(len(c.groups[g]))
		c.groups[g][at] = int32(nextRandom() % values)
	}
	return c
}

func main() {
	cases := make([]kase, 200)
	for i := range cases {
		cases[i] = randomCase(10, 40, 2, 60, i%2 == 1)
	}
	var check int64
	for call := int64(0); call < 200000; call++ {
		c := cases[(check+call*7919)%200]
		r := int64(0)
		if canChoose(c.groups, c.nums) {
			r = 1
		}
		check = (check*31 + r + call%7) % 1000000007
	}
	fmt.Printf("200000 calls over 200 cases: checksum %d\n", check)
}
