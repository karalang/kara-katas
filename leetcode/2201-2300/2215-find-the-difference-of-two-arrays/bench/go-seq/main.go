// LeetCode #2215: Find the Difference of Two Arrays -- bench mirror of
// difference.kara: each array put in a map used as a set, and each list
// the numbers of one set the other lacks.
package main

import "fmt"

func findDifference(nums1, nums2 []int64) [][]int64 {
	first := make(map[int64]struct{})
	second := make(map[int64]struct{})
	for _, x := range nums1 {
		first[x] = struct{}{}
	}
	for _, x := range nums2 {
		second[x] = struct{}{}
	}
	var onlyFirst, onlySecond []int64
	for x := range first {
		if _, ok := second[x]; !ok {
			onlyFirst = append(onlyFirst, x)
		}
	}
	for x := range second {
		if _, ok := first[x]; !ok {
			onlySecond = append(onlySecond, x)
		}
	}
	return [][]int64{onlyFirst, onlySecond}
}

var seed int64 = 2215

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var as, bs [][]int64
	for p := 0; p < 200; p++ {
		// 1000 numbers each, spread over -30..30, -300..300 and -1000..1000
		spread := []int64{30, 300, 1000}[p%3]
		a := make([]int64, 1000)
		for i := range a {
			a[i] = nextRandom()%(2*spread+1) - spread
		}
		b := make([]int64, 1000)
		for i := range b {
			b[i] = nextRandom()%(2*spread+1) - spread
		}
		as = append(as, a)
		bs = append(bs, b)
	}
	var check int64
	for p := 0; p < 200; p++ {
		for r := 0; r < 10; r++ {
			// punch: one number of the first array moves before each answer
			as[p][r*97] = (as[p][r*97]+1001)%2001 - 1000
			for _, list := range findDifference(as[p], bs[p]) {
				// the lists come in any order: their lengths and sums do not
				var sum int64
				for _, x := range list {
					sum += x
				}
				check = (check*31 + int64(len(list))) % 1000000007
				check = (check*31 + sum + 1000000) % 1000000007
			}
		}
	}
	fmt.Printf("200 pairs of 1000, 10 punches: checksum %d\n", check)
}
