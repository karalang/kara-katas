// LeetCode #1784: Check if Binary String Has at Most One Segment of Ones --
// the bench in Go, mirroring check_ones_segment.kara: a search for "01".
package main

import (
	"fmt"
	"strings"
)

func checkOnesSegment(s string) bool {
	return !strings.Contains(s, "01")
}

var seed int64 = 1784

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	list := make([]string, 0, 4000)
	for k := 0; k < 4000; k++ {
		ones := 1 + nextRandom()%100
		s := strings.Repeat("1", int(ones)) + strings.Repeat("0", int(100-ones))
		if k%2 == 1 && ones < 100 {
			at := ones + nextRandom()%(100-ones)
			s = s[:at] + "1" + s[at+1:]
		}
		list = append(list, s)
	}
	var check int64
	for call := int64(0); call < 4000000; call++ {
		s := list[(check+call)%4000]
		if checkOnesSegment(s) {
			check = (check*31 + 2) % 1000000007
		} else {
			check = (check*31 + 1) % 1000000007
		}
	}
	fmt.Printf("4000000 calls over 4000 strings: checksum %d\n", check)
}
