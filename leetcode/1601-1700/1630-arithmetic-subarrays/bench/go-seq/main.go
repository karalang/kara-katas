// LeetCode #1630: Arithmetic Subarrays -- the bench's Go mirror: the ★ arm
// on 200 random problems of 500 numbers and 500 queries, all drawn first.
package main

import (
	"fmt"
	"slices"
)

func checkArithmeticSubarrays(nums, l, r []int32) []bool {
	answers := make([]bool, len(l))
	for q := range l {
		run := slices.Clone(nums[l[q] : r[q]+1])
		slices.Sort(run)
		step := run[1] - run[0]
		ok := true
		for i := 1; i < len(run); i++ {
			if run[i]-run[i-1] != step {
				ok = false
				break
			}
		}
		answers[q] = ok
	}
	return answers
}

var seed int64 = 1630

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type problem struct{ nums, l, r []int32 }
	problems := make([]problem, 200)
	for p := range problems {
		nums := make([]int32, 500)
		for i := range nums {
			if p%2 == 0 {
				nums[i] = int32(3*i - 700)
			} else {
				nums[i] = int32(nextRandom()%200001 - 100000)
			}
		}
		for i := 499; i >= 1; i-- {
			j := nextRandom() % int64(i+1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		l := make([]int32, 500)
		r := make([]int32, 500)
		for q := range l {
			a := nextRandom() % 499
			l[q] = int32(a)
			r[q] = int32(a + 1 + nextRandom()%(499-a))
		}
		problems[p] = problem{nums, l, r}
	}
	var check, yes int64
	for _, p := range problems {
		for _, answer := range checkArithmeticSubarrays(p.nums, p.l, p.r) {
			a := int64(0)
			if answer {
				yes++
				a = 1
			}
			check = (check*31 + a + 1) % 1000000007
		}
	}
	fmt.Printf("200 problems of 500 numbers and 500 queries: %d arithmetic, checksum %d\n", yes, check)
}
