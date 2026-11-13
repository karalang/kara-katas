// LeetCode #1151: Minimum Swaps to Group All 1's Together -- the Go mirror
// of the ★ arm: a window as long as the count of ones slides along the
// list, and the answer is the count less the most ones it holds.
package main

import "fmt"

func minSwaps(data []int64) int64 {
	var k int64
	for _, x := range data {
		k += x
	}
	if k == 0 {
		return 0
	}
	var inside int64
	for i := int64(0); i < k; i++ {
		inside += data[i]
	}
	most := inside
	for i := k; i < int64(len(data)); i++ {
		inside += data[i] - data[i-k]
		if inside > most {
			most = inside
		}
	}
	return k - most
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1151)
	lists := make([][]int64, 16)
	for l := range lists {
		ones := int64(1 + l%7)
		lists[l] = make([]int64, 100000)
		for i := range lists[l] {
			if nextRandom(&seed)%8 < ones {
				lists[l][i] = 1
			}
		}
	}
	var total, check int64
	for r := 0; r < 3000; r++ {
		l := r % 16
		for j := 0; j < 64; j++ {
			at := nextRandom(&seed) * 3
			lists[l][at] = 1 - lists[l][at]
		}
		s := minSwaps(lists[l])
		total += s
		check = (check*31 + s) % 1000000007
	}
	fmt.Printf("3000 rounds over 16 lists of 100000 bits: swaps total %d, checksum %d\n", total, check)
}
