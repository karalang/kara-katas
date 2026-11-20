// LeetCode #1256 bench, in Go: the ★ arm (`num + 1` in binary with its
// leading 1 taken off, the digits found by halving) on 200000 random
// numbers from 0 to 10^9 drawn once, each encoded 20 times; every
// string's length and middle digit folded into a checksum.
package main

import "fmt"

var seed int64 = 1256

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func encode(num int64) string {
	digits := make([]byte, 0, 32)
	x := num + 1
	for x > 1 {
		if x%2 == 1 {
			digits = append(digits, '1')
		} else {
			digits = append(digits, '0')
		}
		x /= 2
	}
	out := make([]byte, len(digits))
	for i := range digits {
		out[i] = digits[len(digits)-1-i]
	}
	return string(out)
}

func main() {
	nums := make([]int64, 0, 200000)
	for i := 0; i < 200000; i++ {
		hi := nextRandom() * 32768
		nums = append(nums, (hi+nextRandom())%1000000001)
	}
	var check int64
	for r := 0; r < 20; r++ {
		for _, num := range nums {
			s := encode(num)
			var mid int64
			if len(s) > 0 {
				if s[len(s)/2] == '1' {
					mid = 2
				} else {
					mid = 1
				}
			}
			check = (check*131 + int64(len(s))*3 + mid) % 1000000007
		}
	}
	fmt.Printf("20 rounds of 200000 numbers: checksum %d\n", check)
}
