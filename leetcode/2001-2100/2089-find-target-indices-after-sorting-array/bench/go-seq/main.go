// LeetCode #2089: Find Target Indices After Sorting Array -- Go mirror of
// the ★ arm's benchmark (target.kara): the same 10000 arrays, each asked for
// every target, two counts and the indices appended to a fresh slice.
package main

import "fmt"

var seed int64 = 2089

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func targetIndices(nums []int64, target int64) []int64 {
	var less, equal int64
	for _, x := range nums {
		if x < target {
			less++
		}
	}
	for _, x := range nums {
		if x == target {
			equal++
		}
	}
	var out []int64
	for i := less; i < less+equal; i++ {
		out = append(out, i)
	}
	return out
}

func main() {
	arrays := make([][]int64, 10000)
	for t := range arrays {
		arrays[t] = make([]int64, 100)
		for i := range arrays[t] {
			arrays[t][i] = nextRandom()%100 + 1
		}
	}
	var total, check int64
	for _, nums := range arrays {
		for target := int64(1); target <= 100; target++ {
			got := targetIndices(nums, target)
			for _, i := range got {
				total += i * target
			}
			var first int64
			if len(got) > 0 {
				first = got[0]
			}
			check = (check*31 + int64(len(got))*100 + first) % 1000000007
		}
	}
	fmt.Printf("1000000 answers: sum %d, checksum %d\n", total, check)
}
