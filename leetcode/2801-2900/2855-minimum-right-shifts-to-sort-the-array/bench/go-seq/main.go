// LeetCode #2855: Minimum Right Shifts to Sort the Array -- the bench:
// the ★ arm over 10^5 arrays of 100 distinct values up to 100,
// LeetCode's most, two times in three sorted and shifted, else with two
// values swapped after it, all drawn first, then each answered 50 times.
package main

import "fmt"

func minimumRightShifts(nums []int64) int64 {
	n := len(nums)
	drop := -1
	for i := 0; i < n-1; i++ {
		if nums[i] > nums[i+1] {
			if drop >= 0 {
				return -1
			}
			drop = i
		}
	}
	if drop < 0 {
		return 0
	}
	if nums[n-1] > nums[0] {
		return -1
	}
	return int64(n - 1 - drop)
}

var seed int64 = 2855

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 100000, 50
	arrays := make([][]int64, 0, count)
	for a := 0; a < count; a++ {
		nums := make([]int64, 100)
		k := int(nextRandom() % 100)
		for i := 0; i < 100; i++ {
			nums[(i+k)%100] = int64(i + 1)
		}
		if nextRandom()%3 == 2 {
			i := nextRandom() % 100
			j := nextRandom() % 100
			nums[i], nums[j] = nums[j], nums[i]
		}
		arrays = append(arrays, nums)
	}
	var sortable, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			shifts := minimumRightShifts(nums)
			if shifts >= 0 {
				sortable++
			}
			check = (check*31 + shifts + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays, %d rounds: %d sortable, checksum %d\n", count, rounds, sortable, check)
}
