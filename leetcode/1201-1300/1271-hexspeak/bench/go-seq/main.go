// LeetCode #1271 bench, in Go: the ★ arm (the decimal text parsed, its
// hexadecimal digits spelled from the lowest, 0 as O, 1 as I, 10 to 15 as A
// to F, any other an error) on 100,000 numbers up to 10^12 drawn once, half
// spelled in the eight letters, 150 rounds; every answer folded into a
// checksum.
package main

import (
	"fmt"
	"strconv"
)

func toHexspeak(num string) string {
	n, _ := strconv.ParseInt(num, 10, 64)
	var letters []byte
	for n > 0 {
		d := n % 16
		switch {
		case d == 0:
			letters = append(letters, 'O')
		case d == 1:
			letters = append(letters, 'I')
		case d >= 10:
			letters = append(letters, byte('A'+d-10))
		default:
			return "ERROR"
		}
		n /= 16
	}
	for i, j := 0, len(letters)-1; i < j; i, j = i+1, j-1 {
		letters[i], letters[j] = letters[j], letters[i]
	}
	return string(letters)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1271)
	letters := []int64{0, 1, 10, 11, 12, 13, 14, 15}
	nums := make([]string, 100000)
	for i := range nums {
		var n int64
		if i%2 == 0 {
			a := nextRandom(&seed)
			b := nextRandom(&seed)
			n = (a*32768+b)%1000000000000 + 1
		} else {
			n = 1
			k := nextRandom(&seed) % 9
			for j := int64(0); j < k; j++ {
				n = n*16 + letters[nextRandom(&seed)%8]
			}
		}
		nums[i] = strconv.FormatInt(n, 10)
	}
	var check int64
	for round := int64(0); round < 150; round++ {
		for _, num := range nums {
			s := toHexspeak(num)
			check = (check*131 + int64(len(s)) + round) % 1000000007
			for i := 0; i < len(s); i++ {
				check = (check*131 + int64(s[i])) % 1000000007
			}
		}
	}
	fmt.Printf("150 rounds of 100000 numbers: checksum %d\n", check)
}
