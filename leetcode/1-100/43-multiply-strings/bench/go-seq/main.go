// LeetCode #43 bench — Go (mirror of multiply_strings.kara).
//
// The digit-grid multiply + digit-table render, building one growing string via
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

func multiply(a, b string) string {
	m := len(a)
	n := len(b)
	res := make([]int64, m+n)
	for i := m - 1; i >= 0; i-- {
		d1 := int64(a[i] - '0')
		for j := n - 1; j >= 0; j-- {
			d2 := int64(b[j] - '0')
			lo := i + j + 1
			hi := i + j
			sum := d1*d2 + res[lo]
			res[lo] = sum % 10
			res[hi] += sum / 10
		}
	}
	k := 0
	for k < len(res) && res[k] == 0 {
		k++
	}
	var sb strings.Builder
	for k < len(res) {
		sb.WriteByte(D[res[k]])
		k++
	}
	if sb.Len() == 0 {
		return "0"
	}
	return sb.String()
}

func main() {
	var total int64 = 300000
	a := "31415926535897932384626433832795028841"
	var out strings.Builder
	for k := int64(0); k < total; k++ {
		v := (k * 2654435761) & 0xffffffff
		b := digitsOf(v)
		out.WriteString(multiply(a, b))
	}
	s := out.String()
	var sum int64 = 0
	for i := 0; i < len(s); i++ {
		sum += int64(s[i])
	}
	fmt.Println(sum)
}
