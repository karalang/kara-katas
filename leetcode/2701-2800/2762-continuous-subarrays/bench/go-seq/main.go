// LeetCode #2762: Continuous Subarrays -- the bench (continuous.kara in
// Go): a window with two deques of indices, each a slice with a head,
// whose fronts are its least and greatest, shrunk from the left while
// those lie more than 2 apart.
package main

import "fmt"

var seed int64 = 2762

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func continuousSubarrays(nums []int64) int64 {
	lows := make([]int, 0, len(nums))
	highs := make([]int, 0, len(nums))
	loHead, hiHead := 0, 0
	left := 0
	var count int64
	for right, v := range nums {
		for len(lows) > loHead && nums[lows[len(lows)-1]] > v {
			lows = lows[:len(lows)-1]
		}
		for len(highs) > hiHead && nums[highs[len(highs)-1]] < v {
			highs = highs[:len(highs)-1]
		}
		lows = append(lows, right)
		highs = append(highs, right)
		for nums[highs[hiHead]]-nums[lows[loHead]] > 2 {
			left++
			if lows[loHead] < left {
				loHead++
			}
			if highs[hiHead] < left {
				hiHead++
			}
		}
		count += int64(right - left + 1)
	}
	return count
}

func main() {
	const count, rounds = 20, 10
	cases := make([][]int64, count)
	for k := range cases {
		value := int64(500000000)
		a := make([]int64, 100000)
		for i := range a {
			value += nextRandom()%5 - 2
			a[i] = value
		}
		cases[k] = a
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range cases {
			found := continuousSubarrays(nums)
			sum += found
			check = (check*31 + found + r) % 1000000007
		}
	}
	fmt.Printf("%d walks of 100000, %d rounds: subarrays sum to %d, checksum %d\n", count, rounds, sum, check)
}
