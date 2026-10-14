// Benchmark for #553: Go mirror of the ★ arm (the shape is always the
// same); see ../optimal_division.kara.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func optimalDivision(nums []int64) string {
	n := len(nums)
	var out strings.Builder
	for i := 0; i < n; i++ {
		if i > 0 {
			out.WriteByte('/')
		}
		if i == 1 && n > 2 {
			out.WriteByte('(')
		}
		out.WriteString(strconv.FormatInt(nums[i], 10))
	}
	if n > 2 {
		out.WriteByte(')')
	}
	return out.String()
}

var seed int64 = 553

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 2000
	all := make([][]int64, count)
	for g := 0; g < count; g++ {
		n := 1 + nextRandom()%10
		nums := make([]int64, 0, n)
		for i := int64(0); i < n; i++ {
			nums = append(nums, 2+nextRandom()%999)
		}
		all[g] = nums
	}
	var chars, checksum int64
	for round := 0; round < 500; round++ {
		for g := 0; g < count; g++ {
			text := optimalDivision(all[(round*7+g)%count])
			chars += int64(len(text))
			checksum = (checksum*31 + int64(len(text)) + int64(text[len(text)/2])) % 1000000007
		}
	}
	fmt.Printf("%d arrays, 500 rounds each: %d characters, checksum %d\n", count, chars, checksum)
}
