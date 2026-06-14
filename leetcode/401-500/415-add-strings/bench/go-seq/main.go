// LeetCode #415 bench — Go (mirror of add_strings.kara).
//
// Two-pointer column add + digit-table render, building one growing string via
// strings.Builder (the String-builder peer), then byte-checksum it.
package main

import (
	"fmt"
	"strings"
)

const D = "0123456789"

func digitsOf(n int64) string {
	if n == 0 {
		return "0"
	}
	v := n
	var buf []int
	for v > 0 {
		buf = append(buf, int(v%10))
		v /= 10
	}
	var sb strings.Builder
	for i := len(buf) - 1; i >= 0; i-- {
		sb.WriteByte(D[buf[i]])
	}
	return sb.String()
}

func addStrings(a, b string) string {
	i := len(a) - 1
	j := len(b) - 1
	var carry int64 = 0
	var buf []int
	for i >= 0 || j >= 0 || carry > 0 {
		sum := carry
		if i >= 0 {
			sum += int64(a[i] - '0')
			i--
		}
		if j >= 0 {
			sum += int64(b[j] - '0')
			j--
		}
		buf = append(buf, int(sum%10))
		carry = sum / 10
	}
	var sb strings.Builder
	for k := len(buf) - 1; k >= 0; k-- {
		sb.WriteByte(D[buf[k]])
	}
	return sb.String()
}

func main() {
	var total int64 = 500000
	a := "31415926535897932384626433832795028841"
	var out strings.Builder
	for k := int64(0); k < total; k++ {
		v := (k * 2654435761) & 0xffffffff
		b := digitsOf(v)
		out.WriteString(addStrings(a, b))
	}
	s := out.String()
	var sum int64 = 0
	for i := 0; i < len(s); i++ {
		sum += int64(s[i])
	}
	fmt.Println(sum)
}
