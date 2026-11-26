package main

import (
	"fmt"
	"strconv"
	"strings"
)

func maxDiff(num int32) int32 {
	s := strconv.Itoa(int(num))
	high := s
	if i := strings.IndexFunc(s, func(c rune) bool { return c != '9' }); i >= 0 {
		high = strings.ReplaceAll(s, s[i:i+1], "9")
	}
	low := s
	if s[0] != '1' {
		low = strings.ReplaceAll(s, s[0:1], "1")
	} else if i := strings.IndexFunc(s[1:], func(c rune) bool { return c != '0' && c != '1' }); i >= 0 {
		low = strings.ReplaceAll(s, s[i+1:i+2], "0")
	}
	a, _ := strconv.Atoi(high)
	b, _ := strconv.Atoi(low)
	return int32(a - b)
}

func main() {
	var seed int64 = 1432
	var check int64 = 0
	for i := 0; i < 3000000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		high := seed / 65536
		seed = (seed*1103515245 + 12345) % 2147483648
		num := int32(1 + (high*32768+seed/65536)%100000000)
		check = (check*131 + int64(maxDiff(num))) % 1000000007
	}
	fmt.Printf("3 * 10^6 numbers: checksum %d\n", check)
}
