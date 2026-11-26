// LeetCode #1417 bench, Go: the letters and the digits apart, each in its
// order, woven together from the larger group, workload and checksum as
// reformat.kara.
package main

import (
	"fmt"
	"strings"
)

func reformat(s string) string {
	var letters, digits []byte
	for i := 0; i < len(s); i++ {
		if s[i] >= 'a' && s[i] <= 'z' {
			letters = append(letters, s[i])
		} else if s[i] >= '0' && s[i] <= '9' {
			digits = append(digits, s[i])
		}
	}
	d := len(letters) - len(digits)
	if d > 1 || d < -1 {
		return ""
	}
	first, second := letters, digits
	if len(digits) > len(letters) {
		first, second = digits, letters
	}
	var out strings.Builder
	for i := range first {
		out.WriteByte(first[i])
		if i < len(second) {
			out.WriteByte(second[i])
		}
	}
	return out.String()
}

func main() {
	var seed int64 = 1417
	letters := []byte{'a', 'b', 'c', 'x', 'y', 'z'}
	var pool strings.Builder
	for i := 0; i < 100000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		r := seed / 65536
		letter := letters[r%6]
		digit := fmt.Sprintf("%d", r/6%10)
		if r/60%2 == 0 {
			pool.WriteByte(letter)
			pool.WriteString(digit)
		} else {
			pool.WriteString(digit)
			pool.WriteByte(letter)
		}
	}
	p := pool.String()
	var check int64
	for w := 0; w < 20000; w++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		start := 2 * (seed / 65536 % 99750)
		out := reformat(p[start : start+500])
		var sum int64
		for k := 0; k < len(out); k++ {
			sum = (sum*31 + int64(out[k])) % 1000000007
		}
		check = (check*131 + sum) % 1000000007
	}
	fmt.Printf("20000 windows of 500 characters: checksum %d\n", check)
}
