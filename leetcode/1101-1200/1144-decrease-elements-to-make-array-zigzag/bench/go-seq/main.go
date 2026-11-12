// LeetCode #1144: Decrease Elements To Make Array Zigzag -- the Go mirror of
// moves_to_make_zigzag.kara: one pass for each choice of which places are
// lowered, each lowered place brought to one below its smaller neighbour;
// the cheaper choice is the answer.
package main

import (
	"fmt"
	"math"
)

func movesToMakeZigzag(nums []int64) int64 {
	n := len(nums)
	best := int64(math.MaxInt64)
	for low := 0; low < 2; low++ {
		var moves int64
		for i := low; i < n; i += 2 {
			least := int64(math.MaxInt64)
			if i > 0 && nums[i-1] < least {
				least = nums[i-1]
			}
			if i+1 < n && nums[i+1] < least {
				least = nums[i+1]
			}
			if nums[i] >= least {
				moves += nums[i] - least + 1
			}
		}
		if moves < best {
			best = moves
		}
	}
	return best
}

var seed int64 = 1144

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 arrays of 1000 values from 1 to 1000, built once. Each of 5000
	// rounds draws one value of every array again and answers every array.
	arrays := make([][]int64, 20)
	for a := range arrays {
		arrays[a] = make([]int64, 1000)
		for i := range arrays[a] {
			arrays[a][i] = nextRandom()%1000 + 1
		}
	}
	var total, check int64
	for r := 0; r < 5000; r++ {
		for a := 0; a < 20; a++ {
			at := nextRandom() % 1000
			arrays[a][at] = nextRandom()%1000 + 1
			answer := movesToMakeZigzag(arrays[a])
			total += answer
			check = (check*131 + answer + 1) % 1000000007
		}
	}
	fmt.Printf("5000 rounds over 20 arrays of 1000 values: answers total %d, checksum %d\n", total, check)
}
