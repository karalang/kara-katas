// Benchmark workload for LeetCode #344 — Go mirror of reverse_string.kara.
package main

import "fmt"

const (
	LEN     = 200000
	PUNCHES = 4000
	MODULUS = 1073741789
)

func reverseString(s []rune) {
	if len(s) < 2 {
		return
	}
	i := 0
	j := len(s) - 1
	for i < j {
		t := s[i]
		s[i] = s[j]
		s[j] = t
		i++
		j--
	}
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func letter(k int64) rune {
	if k < 16 {
		return rune(97 + k)
	}
	return rune(945 + k - 16)
}

func main() {
	var seed int64 = 344
	s := make([]rune, 0)
	for i := 0; i < LEN; i++ {
		s = append(s, letter(next(&seed)%32))
	}
	var sink int64
	for p := 0; p < PUNCHES; p++ {
		pos := (next(&seed)*32768 + next(&seed)) % LEN
		s[pos] = letter(next(&seed) % 32)
		reverseString(s)
		at := (next(&seed)*32768 + next(&seed)) % LEN
		sink = (sink*31 + int64(s[at])) % MODULUS
	}
	fmt.Printf("sink %d\n", sink)
}
