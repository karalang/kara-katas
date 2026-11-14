// LeetCode #2137: Pour Water Between Buckets to Make Water Levels Equal --
// the benchmark, the same algorithm as water.kara. The explicit float64
// conversion keeps Go from fusing the pour's product with the sum: every
// language here rounds the same steps.
package main

import (
	"fmt"
	"math"
)

func equalizeWater(buckets []int64, loss int64) float64 {
	keep := float64(100-loss) / 100.0
	fullest := buckets[0]
	for _, b := range buckets {
		if b > fullest {
			fullest = b
		}
	}
	low, high := 0.0, float64(fullest)
	for k := 0; k < 64; k++ {
		mid := (low + high) / 2.0
		spare, need := 0.0, 0.0
		for _, b := range buckets {
			w := float64(b)
			if w > mid {
				spare += float64((w - mid) * keep)
			} else {
				need += mid - w
			}
		}
		if spare >= need {
			low = mid
		} else {
			high = mid
		}
	}
	return low
}

var seed int64 = 2137

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	lists := make([][]int64, 10)
	for l := 0; l < 10; l++ {
		lists[l] = make([]int64, n)
		for i := 0; i < n; i++ {
			lists[l][i] = nextRandom() % 100001
		}
	}
	total, check := int64(0), int64(0)
	for round := int64(0); round < 10; round++ {
		for l := 0; l < 10; l++ {
			hi := nextRandom()
			at := (hi*32768 + nextRandom()) % n
			lists[l][at] = nextRandom() % 100001
			loss := nextRandom() % 100
			level := equalizeWater(lists[l], loss)
			scaled := int64(math.Floor(level*1048576.0 + 0.5))
			total += scaled
			check = (check*31 + scaled + round) % 1000000007
		}
	}
	fmt.Printf("100 solves: %d in all, in steps of 2^-20, checksum %d\n", total, check)
}
