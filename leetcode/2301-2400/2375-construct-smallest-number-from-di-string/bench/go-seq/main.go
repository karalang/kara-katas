// LeetCode #2375: Construct Smallest Number From DI String -- the bench,
// the ★ arm in Go: the digits 1 to n + 1 pushed on a stack, emptied at
// every I and at the end, so each run of D's comes out falling.
package main

import "fmt"

func smallestNumber(pattern string) string {
	out := []byte{}
	stack := []byte{}
	for i := 0; i <= len(pattern); i++ {
		stack = append(stack, byte('1'+i))
		if i == len(pattern) || pattern[i] == 'I' {
			for len(stack) > 0 {
				out = append(out, stack[len(stack)-1])
				stack = stack[:len(stack)-1]
			}
		}
	}
	return string(out)
}

func main() {
	// every pattern of 1 to 8 letters, 510 in all
	patterns := []string{}
	for n := 1; n < 9; n++ {
		for mask := 0; mask < 1<<n; mask++ {
			letters := make([]byte, n)
			for i := 0; i < n; i++ {
				if (mask>>i)&1 == 1 {
					letters[i] = 'D'
				} else {
					letters[i] = 'I'
				}
			}
			patterns = append(patterns, string(letters))
		}
	}
	check := int64(0)
	for p := int64(0); p < 2000; p++ {
		for _, pattern := range patterns {
			number := smallestNumber(pattern)
			for i := 0; i < len(number); i++ {
				check = (check*31 + int64(number[i]-'0') + p) % 1000000007
			}
		}
	}
	fmt.Printf("2000 passes over 510 patterns: checksum %d\n", check)
}
