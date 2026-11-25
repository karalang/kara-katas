// LeetCode #1363 bench -- Go: the digits counted, the sum's residue put
// right by dropping the smallest one or two digits that do it.
package main

import (
	"fmt"
	"strings"
)

func largestMultipleOfThree(digits []int32) string {
	var count [10]int64
	var sum int64
	for _, d := range digits {
		count[d]++
		sum += int64(d)
	}
	r := sum % 3
	if r != 0 {
		dropped := false
		for d := r; d < 10; d += 3 {
			if count[d] > 0 {
				count[d]--
				dropped = true
				break
			}
		}
		left := 2
		if dropped {
			left = 0
		}
		for d := 3 - r; d < 10; d += 3 {
			for left > 0 && count[d] > 0 {
				count[d]--
				left--
			}
		}
	}
	var out strings.Builder
	for d := 9; d >= 0; d-- {
		for k := int64(0); k < count[d]; k++ {
			out.WriteByte(byte('0' + d))
		}
	}
	s := out.String()
	if strings.HasPrefix(s, "0") {
		return "0"
	}
	return s
}

var seed int64 = 1363

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 arrays of 10^4 digits, the constraints' most, built once; then
	// 10^4 rounds, each setting one digit of one array, both drawn from
	// the checksum so far, and folding the answer's length and three of
	// its digits into the checksum
	arrays := make([][]int32, 20)
	for k := range arrays {
		arrays[k] = make([]int32, 10000)
		for i := range arrays[k] {
			arrays[k][i] = int32(nextRandom() % 10)
		}
	}
	var check int64
	for r := int64(0); r < 10000; r++ {
		k := check % 20
		arrays[k][(check/20)%10000] = int32((check / 200000) % 10)
		answer := largestMultipleOfThree(arrays[k])
		n := int64(len(answer))
		var picks int64
		if n > 0 {
			picks = int64(answer[0])*7 + int64(answer[n/2])*11 + int64(answer[n-1])*13
		}
		check = (check*31 + n + picks + r) % 1000000007
	}
	fmt.Printf("10000 rounds over 20 arrays of 10^4 digits: checksum %d\n", check)
}
