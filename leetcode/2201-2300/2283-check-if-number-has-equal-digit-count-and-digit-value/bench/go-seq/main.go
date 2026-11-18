// LeetCode #2283: Check if Number Has Equal Digit Count and Digit Value
// -- the bench, the ★ arm.
package main

import "fmt"

func digitCount(num string) bool {
	var counts [10]int64
	for _, c := range num {
		counts[c-'0']++
	}
	for i, c := range num {
		if counts[i] != int64(c-'0') {
			return false
		}
	}
	return true
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2283

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	known := []string{"1210", "2020", "21200", "3211000", "42101000", "521001000", "6210001000"}
	nums := make([]string, 0, 100000)
	for k := 0; k < 100000; k++ {
		if k%8 == 0 {
			nums = append(nums, known[nextRandom()%7])
		} else {
			n := nextRandom()%10 + 1
			high := n
			if high > 9 {
				high = 9
			}
			buf := make([]byte, n)
			for j := int64(0); j < n; j++ {
				buf[j] = byte('0' + nextRandom()%(high+1))
			}
			nums = append(nums, string(buf))
		}
	}
	var check int64
	for t := 0; t < 100; t++ {
		var held int64
		for _, num := range nums {
			if digitCount(num) {
				held++
			}
		}
		check = (check*31 + held) % 1000000007
	}
	fmt.Printf("100 passes over 10^5 strings: checksum %d\n", check)
}
