// Benchmark workload for LeetCode #345 — Go mirror of reverse_vowels.kara.
package main

import "fmt"

const (
	LEN     = 200000
	PUNCHES = 1000
	MODULUS = 1073741789
)

func isVowel(c rune) bool {
	switch c {
	case 'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U':
		return true
	}
	return false
}

func reverseVowels(cs []rune) {
	i := 0
	j := len(cs) - 1
	for i < j {
		if !isVowel(cs[i]) {
			i++
		} else if !isVowel(cs[j]) {
			j--
		} else {
			cs[i], cs[j] = cs[j], cs[i]
			i++
			j--
		}
	}
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func letter(k int64) rune {
	if k < 26 {
		return rune(97 + k)
	}
	return rune(65 + k - 26)
}

func main() {
	seed := int64(345)
	s := make([]rune, 0, LEN)
	for i := 0; i < LEN; i++ {
		s = append(s, letter(next(&seed)%32))
	}
	sink := int64(0)
	for p := 0; p < PUNCHES; p++ {
		x := next(&seed)
		y := next(&seed)
		pos := (x*32768 + y) % LEN
		s[pos] = letter(next(&seed) % 32)
		reverseVowels(s)
		u := next(&seed)
		v := next(&seed)
		at := (u*32768 + v) % LEN
		sink = (sink*31 + int64(s[at])) % MODULUS
	}
	fmt.Printf("sink %d\n", sink)
}
