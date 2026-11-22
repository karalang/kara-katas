// LeetCode #2860: Happy Students -- the bench: the ★ arm over 50
// classes of 10^5 students, LeetCode's most, half of them random and
// half built around a group size, all drawn first, then each answered 20
// times, the sort included.
package main

import (
	"fmt"
	"slices"
)

func countWays(nums []int64) int64 {
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	n := int64(len(sorted))
	var ways int64
	for k := int64(0); k <= n; k++ {
		chosenOk := k == 0 || sorted[k-1] < k
		leftOk := k == n || sorted[k] > k
		if chosenOk && leftOk {
			ways++
		}
	}
	return ways
}

var seed int64 = 2860

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func class(n int64) []int64 {
	nums := make([]int64, n)
	if nextRandom()%2 == 0 {
		for i := range nums {
			nums[i] = wide() % n
		}
		return nums
	}
	g := wide() % (n + 1)
	for i := int64(0); i < n; i++ {
		var x int64
		if i < g {
			x = wide() % max(g, 1)
		} else {
			x = g + 1 + wide()%max(n-g, 1)
		}
		nums[i] = min(x, n-1)
	}
	if nextRandom()%4 == 0 {
		at := wide() % n
		nums[at] = min(g, n-1)
	}
	for i := n - 1; i >= 1; i-- {
		j := wide() % (i + 1)
		nums[i], nums[j] = nums[j], nums[i]
	}
	return nums
}

func main() {
	const count, rounds, n = 50, 20, 100000
	classes := make([][]int64, count)
	for c := range classes {
		classes[c] = class(n)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range classes {
			ways := countWays(nums)
			total += ways
			check = (check*31 + ways + r) % 1000000007
		}
	}
	fmt.Printf("%d classes of %d, %d rounds: %d ways, checksum %d\n", count, n, rounds, total, check)
}
