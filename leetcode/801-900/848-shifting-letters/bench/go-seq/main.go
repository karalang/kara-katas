// Benchmark for #848: Shifting Letters -- Go twin of the Kāra ★ arm (suffix
// sums, from the back).
package main

import (
	"fmt"
	"strings"
)

func shiftingLetters(s string, shifts []int64) string {
	b := []byte(s)
	var shift int64
	for i := len(b) - 1; i >= 0; i-- {
		shift = (shift + shifts[i]) % 26
		b[i] = byte('a' + (int64(b[i]-'a')+shift)%26)
	}
	return string(b)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 64, 2000, 100000
	var seed int64 = 848
	texts := make([]string, 0, count)
	allShifts := make([][]int64, 0, count)
	for g := 0; g < count; g++ {
		var sb strings.Builder
		shifts := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			sb.WriteByte(byte('a' + nextRandom(&seed)%26))
			shifts = append(shifts, nextRandom(&seed)*4657%1000000001)
		}
		texts = append(texts, sb.String())
		allShifts = append(allShifts, shifts)
	}
	var checksum int64
	for round := 0; round < rounds; round++ {
		out := shiftingLetters(texts[round%count], allShifts[round%count])
		checksum = (checksum*31 + int64(out[0]) + int64(out[n/2])*7 + int64(out[n-1])*13) % 1000000007
	}
	fmt.Printf("%d rounds of %d strings: checksum %d\n", rounds, count, checksum)
}
