// LeetCode #2075: Decode the Slanted Ciphertext -- Go mirror of the ★ arm's
// benchmark (slanted.kara): 40 grids of 10^6 characters in 1 to 1000 rows,
// built once and decoded.
package main

import (
	"fmt"
	"strings"
)

func decodeCiphertext(text string, rows int) string {
	cols := len(text) / rows
	var plain strings.Builder
	for c := 0; c < cols; c++ {
		for r := 0; r < rows && c+r < cols; r++ {
			plain.WriteByte(text[r*cols+c+r])
		}
	}
	return strings.TrimRight(plain.String(), " ")
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyz      "
	var seed int64 = 2075
	texts := make([]string, 40)
	rowss := make([]int, 40)
	for g := 0; g < 40; g++ {
		rows := []int{1, 2, 10, 100, 1000}[g%5]
		var b strings.Builder
		for i := 0; i < 1000000/rows*rows; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			b.WriteByte(letters[(seed/65536)%32])
		}
		texts[g], rowss[g] = b.String(), rows
	}
	total, check := 0, int64(0)
	for g := range texts {
		plain := decodeCiphertext(texts[g], rowss[g])
		total += len(plain)
		for i := 0; i < len(plain); i++ {
			check = (check*31 + int64(plain[i])) % 1000000007
		}
	}
	fmt.Printf("40 grids: %d characters, checksum %d\n", total, check)
}
