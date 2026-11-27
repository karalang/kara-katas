// LeetCode #1803: Count Pairs With XOR in a Range -- the bench in Go: the ★
// arm over 40 random lists of 20000 numbers built once, 100 calls.
package main

import "fmt"

const bits = 15

func countBelow(nums []int32, limit int32) int64 {
	children := []int64{0, 0}
	counts := []int64{0}
	var pairs int64
	for _, x := range nums {
		node := int64(0)
		for b := bits - 1; b >= 0; b-- {
			xb := int64(x >> b & 1)
			if limit>>b&1 == 1 {
				same := children[2*node+xb]
				if same != 0 {
					pairs += counts[same]
				}
				node = children[2*node+1-xb]
			} else {
				node = children[2*node+xb]
			}
			if node == 0 {
				break
			}
		}
		at := int64(0)
		counts[0]++
		for b := bits - 1; b >= 0; b-- {
			xb := int64(x >> b & 1)
			if children[2*at+xb] == 0 {
				children[2*at+xb] = int64(len(counts))
				counts = append(counts, 0)
				children = append(children, 0, 0)
			}
			at = children[2*at+xb]
			counts[at]++
		}
	}
	return pairs
}

func countPairs(nums []int32, low, high int32) int32 {
	return int32(countBelow(nums, high+1) - countBelow(nums, low))
}

var seed int64 = 1803

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int32, 40)
	for l := range lists {
		lists[l] = make([]int32, 20000)
		for x := range lists[l] {
			lists[l][x] = int32(1 + nextRandom()%20000)
		}
	}
	var check int64
	for call := int64(0); call < 100; call++ {
		low := 1 + nextRandom()%20000
		high := low + nextRandom()%(20001-low)
		check = (check*31 + int64(countPairs(lists[(check+call)%40], int32(low), int32(high)))) % 1000000007
	}
	fmt.Printf("100 calls over 40 lists of 20000 numbers: checksum %d\n", check)
}
