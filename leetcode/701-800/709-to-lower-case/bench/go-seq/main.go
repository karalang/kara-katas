// LeetCode #709: To Lower Case -- character by character.
// Benchmark mirror of the Kara star arm: copy each character into a new
// string, moving 'A' to 'Z' up by 32.
package main

import (
	"fmt"
	"strings"
)

func toLowerCase(s string) string {
	var out strings.Builder
	for _, c := range s {
		if c >= 'A' && c <= 'Z' {
			out.WriteRune(c + 32)
		} else {
			out.WriteRune(c)
		}
	}
	return out.String()
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(709)
	strs := make([]string, 0, 10000)
	for i := 0; i < 10000; i++ {
		var s strings.Builder
		for j := 0; j < 100; j++ {
			s.WriteByte(byte(32 + nextRandom(&seed)%95))
		}
		strs = append(strs, s.String())
	}
	results := make([]string, len(strs))
	copy(results, strs)
	sum := int64(0)
	for round := 0; round < 50; round++ {
		for i := 0; i < 10000; i++ {
			results[i] = toLowerCase(strs[i])
			sum += int64(results[i][(round+i)%100])
		}
	}
	for _, t := range results {
		for j := 0; j < len(t); j++ {
			sum += int64(t[j])
		}
	}
	fmt.Printf("50 rounds of 10000 strings of 100 characters: sum %d\n", sum)
}
