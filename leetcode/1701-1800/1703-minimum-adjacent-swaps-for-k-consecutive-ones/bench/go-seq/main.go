// LeetCode #1703: Minimum Adjacent Swaps for K Consecutive Ones -- the
// bench's Go mirror: the ★ arm on 50 random arrays of 100000 values, each
// with a random k, all drawn first, each answered 40 times.
package main

import (
	"fmt"
	"math"
)

// each window of k ones about its median, q[j] = p[j] - j, by prefix sums
func minMoves(nums []int32, k int32) int32 {
	q := []int64{}
	for i, v := range nums {
		if v == 1 {
			q = append(q, int64(i)-int64(len(q)))
		}
	}
	prefix := []int64{0}
	for _, x := range q {
		prefix = append(prefix, prefix[len(prefix)-1]+x)
	}
	kk := int64(k)
	best := int64(math.MaxInt64)
	for i := int64(0); i <= int64(len(q))-kk; i++ {
		end := i + kk
		m := i + kk/2
		left := q[m]*(m-i) - (prefix[m] - prefix[i])
		right := (prefix[end] - prefix[m+1]) - q[m]*(end-m-1)
		if left+right < best {
			best = left + right
		}
	}
	return int32(best)
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1703

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 50, 40, 100000
	arrays := make([][]int32, 0, count)
	ks := make([]int32, 0, count)
	for c := 0; c < count; c++ {
		// each value a 1 with a chance of its array's own, 1 to 10 in 10
		lean := nextRandom()%10 + 1
		nums := []int32{}
		var ones int64
		for i := 0; i < n; i++ {
			if nextRandom()%10 < lean {
				nums = append(nums, 1)
				ones++
			} else {
				nums = append(nums, 0)
			}
		}
		arrays = append(arrays, nums)
		ks = append(ks, int32(nextRandom()%ones+1))
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for c := range arrays {
			answer := int64(minMoves(arrays[c], ks[c]))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
