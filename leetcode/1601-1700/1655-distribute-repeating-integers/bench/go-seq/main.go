// LeetCode #1655: Distribute Repeating Integers -- the bench's Go mirror:
// the ★ arm on 200 random problems of 100000 numbers from 50 values and
// 10 customers wanting 1 to 3000 each, all drawn first.
package main

import (
	"fmt"
	"math/bits"
)

func canDistribute(nums []int32, quantity []int32) bool {
	counts := map[int32]int64{}
	for _, x := range nums {
		counts[x]++
	}
	m := len(quantity)
	full := (1 << m) - 1
	want := make([]int64, 1<<m)
	for mask := 1; mask <= full; mask++ {
		low := bits.TrailingZeros(uint(mask))
		want[mask] = want[mask&(mask-1)] + int64(quantity[low])
	}
	can := make([]bool, 1<<m)
	before := make([]bool, 1<<m)
	can[0] = true
	for _, count := range counts {
		copy(before, can)
		for mask := 0; mask <= full; mask++ {
			if !before[mask] {
				continue
			}
			rest := full &^ mask
			sub := rest
			for sub > 0 {
				if want[sub] <= count {
					can[mask|sub] = true
				}
				sub = (sub - 1) & rest
			}
		}
	}
	return can[full]
}

var seed int64 = 1655

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type problem struct {
	nums, quantity []int32
}

func main() {
	problems := make([]problem, 0, 200)
	for p := 0; p < 200; p++ {
		nums := make([]int32, 100000)
		for i := range nums {
			nums[i] = int32(nextRandom()%50 + 1)
		}
		quantity := make([]int32, 10)
		for i := range quantity {
			quantity[i] = int32(nextRandom()%3000 + 1)
		}
		problems = append(problems, problem{nums, quantity})
	}
	var check, served int64
	for _, p := range problems {
		answer := canDistribute(p.nums, p.quantity)
		if answer {
			served++
		}
		var v int64 = 1
		if answer {
			v = 2
		}
		check = (check*31 + v) % 1000000007
	}
	fmt.Printf("200 problems of 100000 numbers and 10 customers: %d served, checksum %d\n", served, check)
}
