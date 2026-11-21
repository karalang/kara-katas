// LeetCode #2449: Minimum Number of Operations to Make Arrays Similar --
// the bench, the ★ arm: the odd and the even values of each array sorted
// and matched in order, the distance over 4.
package main

import (
	"fmt"
	"sort"
)

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func makeSimilar(nums, target []int64) int64 {
	var odd, even, oddTarget, evenTarget []int64
	for _, x := range nums {
		if x%2 == 1 {
			odd = append(odd, x)
		} else {
			even = append(even, x)
		}
	}
	for _, x := range target {
		if x%2 == 1 {
			oddTarget = append(oddTarget, x)
		} else {
			evenTarget = append(evenTarget, x)
		}
	}
	for _, s := range [][]int64{odd, even, oddTarget, evenTarget} {
		sort.Slice(s, func(a, b int) bool { return s[a] < s[b] })
	}
	var distance int64
	for i := range odd {
		distance += abs(odd[i] - oddTarget[i])
	}
	for i := range even {
		distance += abs(even[i] - evenTarget[i])
	}
	return distance / 4
}

var seed int64 = 2449

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	r := nextRandom()
	return r*32768 + nextRandom()
}

func main() {
	const n = 100000
	nums := make([]int64, n)
	for i := range nums {
		nums[i] = 1 + wideRandom()%1000000
	}
	target := append([]int64(nil), nums...)
	var check int64
	for p := int64(0); p < 220; p++ {
		for t := 0; t < 1000; t++ {
			i := wideRandom() % n
			j := wideRandom() % n
			step := 2 * (1 + nextRandom()%50)
			if i != j && target[i]+step <= 1000000 && target[j]-step >= 1 {
				target[i] += step
				target[j] -= step
			}
		}
		check = (check*31 + makeSimilar(nums, target) + p) % 1000000007
	}
	fmt.Printf("220 passes over 10^5 values: checksum %d\n", check)
}
