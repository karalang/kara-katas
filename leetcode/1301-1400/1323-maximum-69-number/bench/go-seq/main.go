// LeetCode #1323 bench, Go mirror of the Kāra bench: the ★ arm (the number
// written out, its first 6 turned to a 9, and the text read back) on the 30
// numbers the constraints allow; 100000 passes over all 30, each pass
// starting at a place chosen by the checksum so far and folding every
// answer plus the pass into it.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func maximum69Number(num int32) int32 {
	got, _ := strconv.Atoi(strings.Replace(strconv.Itoa(int(num)), "6", "9", 1))
	return int32(got)
}

func main() {
	var nums []int32
	for digits := 1; digits <= 4; digits++ {
		for pattern := 0; pattern < 1<<digits; pattern++ {
			var num int32
			for k := 0; k < digits; k++ {
				if (pattern>>k)&1 == 1 {
					num = num*10 + 9
				} else {
					num = num*10 + 6
				}
			}
			nums = append(nums, num)
		}
	}
	var check int64
	for pass := int64(0); pass < 100000; pass++ {
		start := check % 30
		for k := int64(0); k < 30; k++ {
			got := int64(maximum69Number(nums[(start+k)%30]))
			check = (check*31 + got + pass) % 1000000007
		}
	}
	fmt.Printf("100000 passes over the 30 numbers: checksum %d\n", check)
}
