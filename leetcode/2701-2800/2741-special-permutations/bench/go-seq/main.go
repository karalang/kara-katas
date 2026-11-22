// LeetCode #2741: Special Permutations -- the bench (special.kara in
// Go): ways[mask][last] carried forward to every partner of `last`.
package main

import (
	"fmt"
	"slices"
)

const mod = 1000000007

func specialPerm(nums []int64) int64 {
	n := len(nums)
	full := (1 << n) - 1
	ways := make([][]int64, 1<<n)
	for i := range ways {
		ways[i] = make([]int64, n)
	}
	for i := 0; i < n; i++ {
		ways[1<<i][i] = 1
	}
	for mask := 1; mask < full; mask++ {
		for last := 0; last < n; last++ {
			w := ways[mask][last]
			if w == 0 {
				continue
			}
			for next := 0; next < n; next++ {
				if (mask>>next)&1 == 0 && (nums[next]%nums[last] == 0 || nums[last]%nums[next] == 0) {
					to := mask | (1 << next)
					ways[to][next] = (ways[to][next] + w) % mod
				}
			}
		}
	}
	var total int64
	for last := 0; last < n; last++ {
		total = (total + ways[full][last]) % mod
	}
	return total
}

var seed int64 = 2741

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 30, 5
	threes := []int64{1, 3, 9, 27}
	arrays := make([][]int64, 0, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, 0, 14)
		for len(nums) < 14 {
			a := nextRandom() % 6
			b := nextRandom() % 4
			x := (int64(1) << a) * threes[b]
			if !slices.Contains(nums, x) {
				nums = append(nums, x)
			}
		}
		arrays = append(arrays, nums)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			k := specialPerm(nums)
			sum += k
			check = (check*31 + k + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 14 numbers, %d rounds: counts sum to %d, checksum %d\n", count, rounds, sum, check)
}
