// LeetCode #1544: Make The String Great -- bench: the ★ arm (a stack of
// runes) over 1000 strings of 1 to 100 letters (the constraint's bound),
// each over its own first 1 to 3 letters in both cases, built once, each
// made great 500 times. Go mirror of great.kara.
package main

import "fmt"

func lower(c rune) rune {
	if c >= 'A' && c <= 'Z' {
		return c | 32
	}
	return c
}

func makeGood(s string) string {
	stack := []rune{}
	for _, c := range s {
		if n := len(stack); n > 0 && stack[n-1] != c && lower(stack[n-1]) == lower(c) {
			stack = stack[:n-1]
		} else {
			stack = append(stack, c)
		}
	}
	return string(stack)
}

var seed int64 = 1544

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	strings := make([]string, 0, 1000)
	for k := 0; k < 1000; k++ {
		n := nextRandom()%100 + 1
		used := nextRandom()%3 + 1
		b := make([]byte, n)
		for i := range b {
			base := byte('A')
			if nextRandom()%2 == 0 {
				base = 'a'
			}
			b[i] = base + byte(nextRandom()%used)
		}
		strings = append(strings, string(b))
	}
	check, total := int64(0), int64(0)
	for p := 0; p < 500; p++ {
		for _, s := range strings {
			great := makeGood(s)
			total += int64(len(great))
			check = mix(check, int64(len(great)))
		}
	}
	fmt.Printf("500 passes over 1000 strings of up to 100 letters: %d letters kept, checksum %d\n", total, check)
}
