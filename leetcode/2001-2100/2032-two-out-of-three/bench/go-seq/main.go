// LeetCode #2032: Two Out of Three -- the ★ arm in Go, the same algorithm
// and workload as three.kara.
package main

import (
	"fmt"
	"math/bits"
)

func twoOutOfThree(nums1, nums2, nums3 []int64) []int64 {
	var mask [101]int64
	for _, x := range nums1 {
		mask[x] |= 1
	}
	for _, x := range nums2 {
		mask[x] |= 2
	}
	for _, x := range nums3 {
		mask[x] |= 4
	}
	out := []int64{}
	for v := int64(1); v < 101; v++ {
		if bits.OnesCount64(uint64(mask[v])) >= 2 {
			out = append(out, v)
		}
	}
	return out
}

var seed int64 = 2032

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	problems := make([][][]int64, 100)
	for p := int64(0); p < 100; p++ {
		problems[p] = make([][]int64, 3)
		for k := 0; k < 3; k++ {
			nums := make([]int64, 100)
			for i := range nums {
				nums[i] = nextRandom()%(p%90+11) + 1
			}
			problems[p][k] = nums
		}
	}
	var calls, kept, check int64
	for round := int64(0); round < 4000; round++ {
		for p := int64(0); p < 100; p++ {
			k := (round + p) % 3
			at := (round*7 + p*13) % 100
			problems[p][k][at] = (problems[p][k][at]+round)%100 + 1
			answer := twoOutOfThree(problems[p][0], problems[p][1], problems[p][2])
			calls++
			kept += int64(len(answer))
			for _, v := range answer {
				check = (check*31 + v) % 1000000007
			}
		}
	}
	fmt.Printf("%d calls: %d values kept, checksum %d\n", calls, kept, check)
}
