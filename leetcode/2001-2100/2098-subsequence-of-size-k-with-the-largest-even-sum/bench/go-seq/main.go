// LeetCode #2098: Subsequence of Size K With the Largest Even Sum -- Go
// mirror of the ★ arm's benchmark (even_sum.kara): the same 200 lists of
// 100000 numbers, each sorted largest first and given the better swap.
package main

import (
	"fmt"
	"sort"
)

func largestEvenSum(nums []int64, k int) int64 {
	sorted := append([]int64(nil), nums...)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i] > sorted[j] })
	var sum int64
	for _, x := range sorted[:k] {
		sum += x
	}
	if sum%2 == 0 {
		return sum
	}
	takenOdd, takenEven := int64(-1), int64(-1)
	for _, x := range sorted[:k] {
		if x%2 == 1 && (takenOdd < 0 || x < takenOdd) {
			takenOdd = x
		}
		if x%2 == 0 && (takenEven < 0 || x < takenEven) {
			takenEven = x
		}
	}
	leftOdd, leftEven := int64(-1), int64(-1)
	for _, x := range sorted[k:] {
		if x%2 == 1 && x > leftOdd {
			leftOdd = x
		}
		if x%2 == 0 && x > leftEven {
			leftEven = x
		}
	}
	best := int64(-1)
	if takenOdd >= 0 && leftEven >= 0 && sum-takenOdd+leftEven > best {
		best = sum - takenOdd + leftEven
	}
	if takenEven >= 0 && leftOdd >= 0 && sum-takenEven+leftOdd > best {
		best = sum - takenEven + leftOdd
	}
	return best
}

var seed int64 = 2098

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func main() {
	var total, check int64
	for r := 0; r < 200; r++ {
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = wideRandom() % 100001
		}
		k := int(wideRandom()%100000 + 1)
		got := largestEvenSum(nums, k)
		total += got
		check = (check*31 + got + 1) % 1000000007
	}
	fmt.Printf("200 answers: sum %d, checksum %d\n", total, check)
}
