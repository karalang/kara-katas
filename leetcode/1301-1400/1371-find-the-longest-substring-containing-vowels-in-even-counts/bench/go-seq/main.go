// LeetCode #1371 bench -- Go: each vowel's count kept as a parity bit, and
// the answer the furthest apart two prefixes with the same bits are.
package main

import "fmt"

func findTheLongestSubstring(s string) int32 {
	var first [32]int64
	for k := range first {
		first[k] = -2
	}
	first[0] = -1
	bits := 0
	var best int64
	for i, c := range s {
		switch c {
		case 'a':
			bits ^= 1
		case 'e':
			bits ^= 2
		case 'i':
			bits ^= 4
		case 'o':
			bits ^= 8
		case 'u':
			bits ^= 16
		}
		if first[bits] == -2 {
			first[bits] = int64(i)
		} else if int64(i)-first[bits] > best {
			best = int64(i) - first[bits]
		}
	}
	return int32(best)
}

var seed int64 = 1371

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 4 strings of 5 * 10^5 letters, the constraints' most, drawn from
	// "aeioubcxyz", built once; then 80 rounds, each changing one letter
	// of one string to a copy, both drawn from the checksum so far, and
	// finding that string's longest substring
	pool := "aeioubcxyz"
	strs := make([]string, 4)
	for k := range strs {
		b := make([]byte, 500000)
		for j := range b {
			b[j] = pool[nextRandom()%10]
		}
		strs[k] = string(b)
	}
	var check int64
	for r := int64(0); r < 80; r++ {
		i := check % 4
		at := (check / 4) % 500000
		b := []byte(strs[i])
		b[at] = pool[(check/2000000)%10]
		strs[i] = string(b)
		got := int64(findTheLongestSubstring(strs[i]))
		check = (check*31 + got + r) % 1000000007
	}
	fmt.Printf("80 rounds over 4 strings of 500000 letters: checksum %d\n", check)
}
