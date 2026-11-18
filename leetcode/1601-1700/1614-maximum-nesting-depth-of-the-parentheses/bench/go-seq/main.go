// LeetCode #1614: Maximum Nesting Depth of the Parentheses -- the bench in
// Go, mirroring depth.kara: one pass counting the parentheses open,
// keeping the most.
package main

import (
	"fmt"
	"strings"
)

func maxDepth(s string) int32 {
	var open, most int32
	for _, c := range s {
		if c == '(' {
			open++
			if open > most {
				most = open
			}
		} else if c == ')' {
			open--
		}
	}
	return most
}

var seed int64 = 1614

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func expression(size int64, out *strings.Builder) {
	left := size
	for {
		if left > 1 && nextRandom()%3 == 0 {
			inner := nextRandom()%left + 1
			out.WriteByte('(')
			expression(inner, out)
			out.WriteByte(')')
			left -= inner
		} else {
			out.WriteByte(byte('0' + nextRandom()%10))
			left--
		}
		if left <= 0 {
			break
		}
		out.WriteByte("+-*/"[nextRandom()%4])
	}
}

func main() {
	var expressions []string
	for e := 0; e < 10; e++ {
		var b strings.Builder
		expression(200000, &b)
		expressions = append(expressions, b.String())
	}
	var check, chars int64
	for _, s := range expressions {
		for k := 0; k < 10; k++ {
			check = (check*31 + int64(maxDepth(s)) + 1) % 1000000007
			chars += int64(len(s))
		}
	}
	fmt.Printf("10 expressions of 200000 terms, each read 10 times: %d characters, checksum %d\n", chars, check)
}
