// LeetCode #1415 bench, Go: the first letter from (k - 1) / 2^(n - 1), and
// each letter after it the lower or the higher of the two that differ from
// the one before, workload and checksum as get_happy_string.kara.
package main

import (
	"fmt"
	"strings"
)

func getHappyString(n, k int32) string {
	perFirst := int32(1) << (n - 1)
	if k > 3*perFirst {
		return ""
	}
	letters := []byte{'a', 'b', 'c'}
	rest := k - 1
	last := letters[rest/perFirst]
	rest %= perFirst
	var s strings.Builder
	s.WriteByte(last)
	for bit := perFirst / 2; bit > 0; bit /= 2 {
		options := make([]byte, 0, 2)
		for _, c := range letters {
			if c != last {
				options = append(options, c)
			}
		}
		if rest >= bit {
			last = options[1]
			rest -= bit
		} else {
			last = options[0]
		}
		s.WriteByte(last)
	}
	return s.String()
}

func main() {
	var seed int64 = 1415
	var check int64
	for r := 0; r < 1000000; r++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		n := 1 + seed/65536%10
		k := 1 + seed/1024%100
		s := getHappyString(int32(n), int32(k))
		var sum int64
		for i := 0; i < len(s); i++ {
			sum = sum*3 + int64(s[i])
		}
		check = (check*131 + sum + int64(len(s))) % 1000000007
	}
	fmt.Printf("10^6 cases: checksum %d\n", check)
}
