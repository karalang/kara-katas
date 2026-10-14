// Benchmark for #564: Go mirror of the ★ arm (five candidates); see
// ../nearest_palindromic.kara.
package main

import (
	"fmt"
	"strconv"
)

func pow10(e int64) int64 {
	r := int64(1)
	for i := int64(0); i < e; i++ {
		r *= 10
	}
	return r
}

func mirrored(half, length int64) int64 {
	text := strconv.FormatInt(half, 10)
	s := []byte(text)
	i := min(length/2, int64(len(text))) - 1
	for i >= 0 {
		s = append(s, text[i])
		i--
	}
	r, _ := strconv.ParseInt(string(s), 10, 64)
	return r
}

func abs64(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func nearestPalindromic(n string) string {
	value, _ := strconv.ParseInt(n, 10, 64)
	length := int64(len(n))
	half, _ := strconv.ParseInt(n[:(length+1)/2], 10, 64)
	candidates := []int64{pow10(length-1) - 1, pow10(length) + 1}
	for _, h := range []int64{half - 1, half, half + 1} {
		candidates = append(candidates, mirrored(h, length))
	}
	best := int64(-1)
	for _, c := range candidates {
		if c == value || c < 0 {
			continue
		}
		d := abs64(c - value)
		bd := abs64(best - value)
		if best == -1 || d < bd || (d == bd && c < best) {
			best = c
		}
	}
	return strconv.FormatInt(best, 10)
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomNumber(t int64, seed *int64) string {
	length := 1 + step(seed)%18
	digits := []int64{1 + step(seed)%9}
	for i := int64(1); i < length; i++ {
		digits = append(digits, step(seed)%10)
	}
	if t%3 == 1 {
		for i := int64(0); i < length/2; i++ {
			digits[length-1-i] = digits[i]
		}
	}
	var value int64
	for _, d := range digits {
		value = value*10 + d
	}
	if t%3 == 2 {
		value = pow10(length-1) + step(seed)%7 - 3
		if value < 1 {
			value = 1
		}
	}
	return strconv.FormatInt(value, 10)
}

func main() {
	count := int64(10000)
	rounds := int64(300)
	seed := int64(564)
	numbers := make([]string, 0, count)
	for t := int64(0); t < count; t++ {
		numbers = append(numbers, randomNumber(t, &seed))
	}
	var checksum int64
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			got, _ := strconv.ParseInt(nearestPalindromic(numbers[(round*7+g)%count]), 10, 64)
			checksum = (checksum*31 + got%1000000007) % 1000000007
		}
	}
	fmt.Printf("%d numbers, %d rounds: checksum %d\n", count, rounds, checksum)
}
