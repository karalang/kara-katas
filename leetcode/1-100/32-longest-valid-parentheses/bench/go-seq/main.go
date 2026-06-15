// LeetCode #32 bench — Go (mirror of longest_valid_parentheses.kara).
//
// The index-stack longest-valid-parens, stack allocated fresh per call; sliding
// window over a fixed pseudo-random parens buffer, folded to a checksum (single
// goroutine — seq lane).
package main

import "fmt"

func longestValidWindow(buf []byte, start, w int64) int64 {
	stack := make([]int64, 0, w+1)
	stack = append(stack, -1)
	var best int64 = 0
	for i := int64(0); i < w; i++ {
		if buf[start+i] == '(' {
			stack = append(stack, i)
		} else {
			stack = stack[:len(stack)-1] // pop
			if len(stack) == 0 {
				stack = append(stack, i)
			} else {
				top := stack[len(stack)-1]
				if l := i - top; l > best {
					best = l
				}
			}
		}
	}
	return best
}

func main() {
	const bigL int64 = 4096
	const w int64 = 2048
	const total int64 = 330000
	const modulus int64 = 1000000007

	buf := make([]byte, 0, bigL)
	var x int64 = 0x12345
	for p := int64(0); p < bigL; p++ {
		x = (x*1103515245 + 12345) & 0x7fffffff
		if (x & 1) == 0 {
			buf = append(buf, '(')
		} else {
			buf = append(buf, ')')
		}
	}

	span := bigL - w + 1
	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		start := (k * 7) % span
		r := longestValidWindow(buf, start, w)
		acc = (acc + r) % modulus
	}

	fmt.Println(acc)
}
