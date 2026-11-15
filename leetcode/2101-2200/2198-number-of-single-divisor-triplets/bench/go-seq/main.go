// benchmark's Go mirror of count.kara (LeetCode #2198, the ★ arm): every
// ordered triple of the values held.
package main

import "fmt"

func singleDivisorTriplet(nums []int64) int64 {
	var count [101]int64
	for _, x := range nums {
		count[x]++
	}
	var total int64
	for a := int64(1); a < 101; a++ {
		if count[a] == 0 {
			continue
		}
		for b := int64(1); b < 101; b++ {
			if count[b] == 0 {
				continue
			}
			for c := int64(1); c < 101; c++ {
				if count[c] == 0 {
					continue
				}
				sum := a + b + c
				byA, byB, byC := sum%a == 0, sum%b == 0, sum%c == 0
				if (byA && !byB && !byC) || (byB && !byA && !byC) || (byC && !byA && !byB) {
					second := count[b]
					if b == a {
						second--
					}
					third := count[c]
					if c == a {
						third--
					}
					if c == b {
						third--
					}
					total += count[a] * second * third
				}
			}
		}
	}
	return total
}

var seed int64 = 2198

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := [][]int64{}
	for a := 0; a < 20; a++ {
		top := int64(81 + a)
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = nextRandom()%top + 1
		}
		arrays = append(arrays, nums)
	}
	var check int64
	for pass := 0; pass < 10; pass++ {
		for _, nums := range arrays {
			check = (check*31 + singleDivisorTriplet(nums)%1000000007) % 1000000007
		}
	}
	fmt.Printf("10 passes over 20 arrays: checksum %d\n", check)
}
