// LeetCode #2219: Maximum Sum Score of Array -- bench mirror of
// score.kara: with the total known, one pass keeps the sum before i, and
// the sum from i on is the total less it.
package main

import "fmt"

func maximumSumScore(nums []int64) int64 {
	var total int64
	for _, x := range nums {
		total += x
	}
	var before int64
	// no score is below the smaller of the first number and the total
	best := nums[0]
	if total < best {
		best = total
	}
	for _, x := range nums {
		fromHere := total - before
		before += x
		if before > best {
			best = before
		}
		if fromHere > best {
			best = fromHere
		}
	}
	return best
}

var seed int64 = 2219

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// a draw of 30 bits, since one draw stops at 32767
func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	var arrays [][]int64
	for a := 0; a < 30; a++ {
		// 10^5 numbers from -10^5 to 10^5
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = wideRandom()%200001 - 100000
		}
		arrays = append(arrays, nums)
	}
	var check int64
	for a := 0; a < 30; a++ {
		for r := 0; r < 10; r++ {
			// punch: one number is drawn again before each answer
			arrays[a][r*9999] = wideRandom()%200001 - 100000
			check = (check*31 + maximumSumScore(arrays[a]) + 10000000000) % 1000000007
		}
	}
	fmt.Printf("30 arrays of 10^5, 10 punches: checksum %d\n", check)
}
