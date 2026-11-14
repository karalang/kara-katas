// LeetCode #2161: Partition Array According to Given Pivot -- the
// benchmark's Go mirror of pivot.kara.
package main

import "fmt"

func pivotArray(nums []int64, pivot int64) []int64 {
	out := make([]int64, 0, len(nums))
	for _, x := range nums {
		if x < pivot {
			out = append(out, x)
		}
	}
	for _, x := range nums {
		if x == pivot {
			out = append(out, x)
		}
	}
	for _, x := range nums {
		if x > pivot {
			out = append(out, x)
		}
	}
	return out
}

var seed int64 = 2161

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	lists := make([][]int64, 4)
	for l := range lists {
		lists[l] = make([]int64, 100000)
		for i := range lists[l] {
			lists[l][i] = wideRandom()%2000001 - 1000000
		}
	}
	var check int64
	for round := int64(0); round < 25; round++ {
		for l := 0; l < 4; l++ {
			at := wideRandom() % 100000
			lists[l][at] = wideRandom()%2000001 - 1000000
			pivot := lists[l][wideRandom()%100000]
			out := pivotArray(lists[l], pivot)
			for k := 0; k < 10; k++ {
				check = (check*31 + out[k*9999] + 1000001 + round) % 1000000007
			}
		}
	}
	fmt.Printf("100 solves: checksum %d\n", check)
}
