// LeetCode #2155: All Divisions With the Highest Score of a Binary Array
// -- the benchmark's Go mirror of divisions.kara.
package main

import "fmt"

func maxScoreIndices(nums []int64) []int64 {
	var rightOnes int64
	for _, x := range nums {
		if x == 1 {
			rightOnes++
		}
	}
	var leftZeros int64
	top := rightOnes
	found := []int64{0}
	for i, x := range nums {
		if x == 0 {
			leftZeros++
		} else {
			rightOnes--
		}
		score := leftZeros + rightOnes
		if score > top {
			top = score
			found = found[:0]
		}
		if score == top {
			found = append(found, int64(i)+1)
		}
	}
	return found
}

var seed int64 = 2155

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int64, 4)
	for s := range lists {
		lists[s] = make([]int64, 100000)
		for i := range lists[s] {
			lists[s][i] = nextRandom() % 2
		}
	}
	var total, check int64
	for round := int64(0); round < 50; round++ {
		for s := 0; s < 4; s++ {
			at := nextRandom() % 100000
			lists[s][at] = 1 - lists[s][at]
			out := maxScoreIndices(lists[s])
			n := int64(len(out))
			total += n
			check = (check*31 + n + out[0] + out[n-1] + round) % 1000000007
		}
	}
	fmt.Printf("200 solves: %d divisions in all, checksum %d\n", total, check)
}
