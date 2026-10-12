// Benchmark for #443: mirror of compress.kara (reading and writing in
// place) on 1,000 random strings of 2,000 characters, built once, copied
// and compressed 20 times over.
package main

import (
	"fmt"
	"strconv"
)

func compress(chars []rune) int {
	n := len(chars)
	read, write := 0, 0
	for read < n {
		c := chars[read]
		start := read
		for read < n && chars[read] == c {
			read++
		}
		chars[write] = c
		write++
		count := read - start
		if count > 1 {
			for _, digit := range strconv.Itoa(count) {
				chars[write] = digit
				write++
			}
		}
	}
	return write
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, size, rounds = 1000, 2000, 20
	longests := []int64{1, 3, 15, 120}
	seed := int64(443)
	// Runs of 1 to 1, 3, 15 or 120 letters from a three-letter alphabet.
	strings := [][]rune{}
	for s := 0; s < count; s++ {
		longest := longests[nextRandom(&seed)%4]
		chars := []rune{}
		for len(chars) < size {
			c := rune('a' + nextRandom(&seed)%3)
			run := 1 + nextRandom(&seed)%longest
			for r := int64(0); r < run; r++ {
				if len(chars) < size {
					chars = append(chars, c)
				}
			}
		}
		strings = append(strings, chars)
	}
	length := 0
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		for s := 0; s < count; s++ {
			chars := append([]rune(nil), strings[s]...)
			n := compress(chars)
			length += n
			checksum = (checksum*31 + int64(n) + int64(chars[n-1]) + round) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d strings of %d: compressed length %d, checksum %d\n", rounds, count, size, length, checksum)
}
