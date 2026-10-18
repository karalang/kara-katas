// LeetCode 753 — Cracking the Safe, bench: the ★ arm (an Euler circuit
// by Hierholzer's method), mirrored from crack_safe.kara.
package main

import (
	"fmt"
	"strings"
)

type entry struct{ node, digit int64 }

func crackSafe(n, k int64) string {
	nodes := int64(1)
	for i := int64(0); i < n-1; i++ {
		nodes *= k
	}
	used := make([]int64, nodes)
	stack := []entry{{0, -1}}
	digits := []int64{}
	for len(stack) > 0 {
		top := stack[len(stack)-1]
		if used[top.node] < k {
			d := used[top.node]
			used[top.node]++
			stack = append(stack, entry{(top.node*k + d) % nodes, d})
		} else {
			stack = stack[:len(stack)-1]
			if top.digit >= 0 {
				digits = append(digits, top.digit)
			}
		}
	}
	var out strings.Builder
	for i := int64(0); i < n-1; i++ {
		out.WriteByte('0')
	}
	for i := len(digits) - 1; i >= 0; i-- {
		out.WriteByte(byte('0' + digits[i]))
	}
	return out.String()
}

func main() {
	rounds := 2000
	var safes, digits, check int64
	for r := 0; r < rounds; r++ {
		for n := int64(1); n < 5; n++ {
			for k := int64(1); k < 11; k++ {
				total := int64(1)
				for i := int64(0); i < n; i++ {
					total *= k
				}
				if total <= 4096 {
					safes++
					text := crackSafe(n, k)
					digits += int64(len(text))
					for i := 0; i < len(text); i++ {
						check = (check*31 + int64(text[i])) % 1000000007
					}
				}
			}
		}
	}
	fmt.Printf("%d safes: %d digits in all, checksum %d\n", safes, digits, check)
}
