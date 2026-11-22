// LeetCode #2708: Maximum Strength of a Group -- the bench (strength.kara
// in Go): every non-zero number multiplied in, and an odd negative, the
// one nearest zero, divided back out.
package main

import "fmt"

func maxStrength(nums []int64) int64 {
	if len(nums) == 1 {
		return nums[0]
	}
	product, taken, negatives, nearest := int64(1), 0, 0, int64(-10)
	for _, v := range nums {
		if v != 0 {
			product *= v
			taken++
		}
		if v < 0 {
			negatives++
			if v > nearest {
				nearest = v
			}
		}
	}
	if negatives%2 == 1 {
		product /= nearest
		taken--
	}
	if taken > 0 {
		return product
	}
	return 0
}

var seed int64 = 2708

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	groups, rounds := 1000000, 10
	all := make([][]int64, groups)
	for g := range all {
		n := nextRandom()%13 + 1
		all[g] = make([]int64, n)
		for i := range all[g] {
			all[g][i] = nextRandom()%19 - 9
		}
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, nums := range all {
			strength := maxStrength(nums)
			sum += strength % 1000
			check = (check*31 + (strength%1000000007+1000000007)%1000000007 + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d groups of 1 to 13, %d rounds: strengths mod 1000 sum to %d, checksum %d\n", groups, rounds, sum, check)
}
