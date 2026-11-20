// LeetCode #1250 bench, in Go: the ★ arm (Euclid's algorithm folded over
// the array, stopping once the divisor reaches 1) on 50 random arrays of
// 100000 values built once, every value sharing a factor from 2 to 1000
// and, in half of them, one value of no shared factor put in at a random
// place; each asked 20 times, every answer folded into a checksum.
package main

import "fmt"

var seed int64 = 1250

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func bigRandom() int64 {
	hi := nextRandom() * 32768
	return hi + nextRandom()
}

func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func isGoodArray(nums []int64) bool {
	var g int64
	for _, x := range nums {
		g = gcd(g, x)
		if g == 1 {
			return true
		}
	}
	return g == 1
}

func main() {
	arrays := make([][]int64, 0, 50)
	for t := 0; t < 50; t++ {
		factor := nextRandom()%999 + 2
		nums := make([]int64, 100000)
		for i := range nums {
			nums[i] = factor * (bigRandom()%(1000000000/factor) + 1)
		}
		if t%2 == 0 {
			nums[bigRandom()%100000] = 999999937
		}
		arrays = append(arrays, nums)
	}
	var check int64
	for r := 0; r < 20; r++ {
		for t, nums := range arrays {
			yes := isGoodArray(nums)
			add := int64(0)
			if yes {
				add = int64(t) + 1
			}
			check = (check*131 + add) % 1000000007
		}
	}
	fmt.Printf("20 rounds of 50 arrays of 100000 values: checksum %d\n", check)
}
