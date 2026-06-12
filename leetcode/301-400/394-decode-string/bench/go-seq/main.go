// LeetCode #394 bench harness — Go peer (go build, single-thread).
//
// Same iterative-stack byte-scan decode as the Kāra mirror; `cur*count` uses
// strings.Repeat (Kāra's String.repeat analog). Sink = ITERS * 52 = 41600000.
package main

import (
	"fmt"
	"strings"
)

const (
	encoded = "3[ab2[cd]ef]5[gh]2[ij3[kl]m]"
	iters   = 800000
)

func isLetter(b byte) bool {
	return b != '[' && b != ']' && !(b >= '0' && b <= '9')
}

func decodeString(s string) string {
	var strStack []string
	var numStack []int64
	cur := ""
	var k int64 = 0
	n := len(s)
	i := 0
	for i < n {
		b := s[i]
		if b >= '0' && b <= '9' {
			k = k*10 + int64(b-'0')
			i++
		} else if b == '[' {
			strStack = append(strStack, cur)
			numStack = append(numStack, k)
			cur = ""
			k = 0
			i++
		} else if b == ']' {
			count := numStack[len(numStack)-1]
			numStack = numStack[:len(numStack)-1]
			prev := strStack[len(strStack)-1]
			strStack = strStack[:len(strStack)-1]
			cur = prev + strings.Repeat(cur, int(count))
			i++
		} else {
			j := i
			for j < n && isLetter(s[j]) {
				j++
			}
			cur += s[i:j]
			i = j
		}
	}
	return cur
}

func main() {
	var sum int64
	for it := 0; it < iters; it++ {
		sum += int64(len(decodeString(encoded)))
	}
	fmt.Println(sum)
}
