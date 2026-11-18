// LeetCode #2226: Maximum Candies Allocated to K Children -- the
// benchmark's Go mirror of candies.kara: a binary search on the answer,
// x candies each possible when the piles give k shares of x.
package main

import "fmt"

func maximumCandies(candies []int64, k int64) int64 {
	var low, high int64
	for _, pile := range candies {
		if pile > high {
			high = pile
		}
	}
	for low < high {
		x := (low + high + 1) / 2
		var shares int64
		for _, pile := range candies {
			shares += pile / x
		}
		if shares >= k {
			low = x
		} else {
			high = x - 1
		}
	}
	return low
}

var seed int64 = 2226

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	lists := make([][]int64, 4)
	for l := range lists {
		lists[l] = make([]int64, 100000)
		for i := range lists[l] {
			lists[l][i] = wideRandom()%10000000 + 1
		}
	}
	children := []int64{1000, 1000000, 1000000000, 100000000000}
	var check int64
	for r := 0; r < 25; r++ {
		for l := 0; l < 4; l++ {
			// punch: one pile is drawn again before each answer
			at := wideRandom() % 100000
			lists[l][at] = wideRandom()%10000000 + 1
			check = (check*31 + maximumCandies(lists[l], children[l])) % 1000000007
		}
	}
	fmt.Printf("100 answers over 10^5 piles: checksum %d\n", check)
}
