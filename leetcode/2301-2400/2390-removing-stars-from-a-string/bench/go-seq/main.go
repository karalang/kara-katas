// LeetCode #2390: Removing Stars From a String -- the bench, the ★ arm in
// Go: a stack, a letter pushed and a star popping.
package main

import "fmt"

var seed int64 = 2390

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func starred(length, odds int64) string {
	out := make([]byte, 0, length)
	depth := 0
	for i := int64(0); i < length; i++ {
		if depth > 0 && nextRandom()%odds == 0 {
			out = append(out, '*')
			depth--
		} else {
			out = append(out, byte('a'+nextRandom()%26))
			depth++
		}
	}
	return string(out)
}

func removeStars(s string) string {
	stack := []byte{}
	for i := 0; i < len(s); i++ {
		if s[i] == '*' {
			if len(stack) > 0 {
				stack = stack[:len(stack)-1]
			}
		} else {
			stack = append(stack, s[i])
		}
	}
	return string(stack)
}

func main() {
	strings := make([]string, 20)
	for i := range strings {
		strings[i] = starred(100000, 3)
	}
	var check int64
	for p := int64(0); p < 100; p++ {
		for _, s := range strings {
			t := removeStars(s)
			for i := 0; i < len(t); i++ {
				check = (check*31 + int64(t[i]-'a'+1)) % 1000000007
			}
			check = (check*31 + int64(len(t)) + p) % 1000000007
		}
	}
	fmt.Printf("100 passes over 20 strings of 10^5 characters: checksum %d\n", check)
}
