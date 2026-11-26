// LeetCode #1449 Form Largest Integer With Digits That Add up to Target: the
// bench, a mirror of largest_number.kara.
package main

import (
	"fmt"
	"strings"
)

func largestNumber(cost []int, target int) string {
	// the most digits each cost from 0 to target buys exactly, -1 when it
	// buys none; then the digits taken from 9 down, each while what is
	// left still buys one digit fewer
	most := make([]int64, target+1)
	for t := range most {
		most[t] = -1
	}
	most[0] = 0
	for t := 1; t <= target; t++ {
		for _, c := range cost {
			if c <= t && most[t-c] >= 0 {
				most[t] = max(most[t], most[t-c]+1)
			}
		}
	}
	if most[target] < 0 {
		return "0"
	}
	var digits strings.Builder
	left := target
	for d := 8; d >= 0; d-- {
		c := cost[d]
		for c <= left && most[left-c] == most[left]-1 {
			digits.WriteByte(byte('1' + d))
			left -= c
		}
	}
	return digits.String()
}

func main() {
	// 5000 cases with the constraints' most target, 5000, each with nine
	// costs drawn from 1 to 50, each answer's digits folded to a checksum
	var seed int64 = 1449
	var check int64 = 0
	for r := 0; r < 5000; r++ {
		cost := make([]int, 0, 9)
		for i := 0; i < 9; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			cost = append(cost, int(1+seed/65536%50))
		}
		s := largestNumber(cost, 5000)
		for i := 0; i < len(s); i++ {
			check = (check*131 + int64(s[i])) % 1000000007
		}
	}
	fmt.Printf("5000 targets of 5000: checksum %d\n", check)
}
