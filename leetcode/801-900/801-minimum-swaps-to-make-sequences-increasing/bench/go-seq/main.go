// LeetCode 801 — Minimum Swaps To Make Sequences Increasing: the bench,
// in Go. Mirrors min_swap.kara: two states, left alone and swapped.
package main

import "fmt"

func minSwap(nums1, nums2 []int64) int64 {
	n := int64(len(nums1))
	var keep, swap int64 = 0, 1
	for i := int64(1); i < n; i++ {
		same := nums1[i-1] < nums1[i] && nums2[i-1] < nums2[i]
		cross := nums1[i-1] < nums2[i] && nums2[i-1] < nums1[i]
		nextKeep, nextSwap := n+1, n+1
		if same {
			nextKeep, nextSwap = keep, swap+1
		}
		if cross {
			nextKeep = min(nextKeep, swap)
			nextSwap = min(nextSwap, keep+1)
		}
		keep, swap = nextKeep, nextSwap
	}
	return min(keep, swap)
}

var seed int64 = 801

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 100000
	as := make([][]int64, 16)
	bs := make([][]int64, 16)
	for p := 0; p < 16; p++ {
		a := make([]int64, 0, n)
		b := make([]int64, 0, n)
		var x, y int64
		for i := int64(0); i < n; i++ {
			x += 1 + nextRandom()%2
			y += 1 + nextRandom()%2
			if nextRandom()%2 == 0 {
				a = append(a, x)
				b = append(b, y)
			} else {
				a = append(a, y)
				b = append(b, x)
			}
		}
		as[p], bs[p] = a, b
	}
	var rounds int64 = 2000
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		k := minSwap(as[r%16], bs[r%16])
		total += k
		check = (check*131 + k) % 1000000007
	}
	fmt.Printf("%d rounds of %d places: %d swaps in all, checksum %d\n", rounds, n, total, check)
}
