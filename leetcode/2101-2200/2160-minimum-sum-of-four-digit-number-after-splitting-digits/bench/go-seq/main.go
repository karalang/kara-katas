// LeetCode #2160: Minimum Sum of Four Digit Number After Splitting Digits
// -- the benchmark's Go mirror of digits.kara.
package main

import (
	"fmt"
	"sort"
	"strconv"
)

func minimumSum(num int64) int64 {
	text := strconv.FormatInt(num, 10)
	d := make([]int64, len(text))
	for i := 0; i < len(text); i++ {
		d[i] = int64(text[i] - '0')
	}
	sort.Slice(d, func(i, j int) bool { return d[i] < d[j] })
	return (d[0]*10 + d[2]) + (d[1]*10 + d[3])
}

func main() {
	var total, check int64
	for pass := int64(0); pass < 200; pass++ {
		for k := int64(0); k < 9000; k++ {
			num := 1000 + (k+37*pass)%9000
			sum := minimumSum(num)
			total += sum
			check = (check*31 + sum + pass) % 1000000007
		}
	}
	fmt.Printf("1800000 solves: %d in all, checksum %d\n", total, check)
}
