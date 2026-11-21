// LeetCode #2496: Maximum Value of a String in an Array -- Go mirror of
// the benchmark (value.kara): the same lists, passes and checksum; the
// checksum written with strconv.
package main

import (
	"fmt"
	"strconv"
)

var seed int64 = 2496

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func maximumValue(strs []string) int64 {
	var best int64
	for _, s := range strs {
		var number int64
		digits := true
		for _, c := range s {
			if c >= '0' && c <= '9' {
				number = number*10 + int64(c-'0')
			} else {
				digits = false
			}
		}
		worth := int64(len(s))
		if digits {
			worth = number
		}
		if worth > best {
			best = worth
		}
	}
	return best
}

func main() {
	const passes int64 = 90
	lists := make([][]string, 2000)
	for l := range lists {
		strs := make([]string, 100)
		for i := range strs {
			length := nextRandom()%9 + 1
			b := make([]byte, length)
			for j := range b {
				k := nextRandom()
				if k%2 == 0 {
					b[j] = byte('0' + k/2%10)
				} else {
					b[j] = byte('a' + k/2%26)
				}
			}
			strs[i] = string(b)
		}
		lists[l] = strs
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for l := 0; l < 2000; l++ {
			at := check % 100
			was := lists[l][at]
			lists[l][at] = strconv.FormatInt(check%1000000000, 10)
			check = (check*31 + maximumValue(lists[l]) + p) % 1000000007
			lists[l][at] = was
		}
	}
	fmt.Printf("%d passes over 2000 lists of 100: checksum %d\n", passes, check)
}
