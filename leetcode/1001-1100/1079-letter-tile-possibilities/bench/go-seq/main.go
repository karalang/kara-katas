// LeetCode #1079 bench: the Go mirror of tiles.kara, the same walk over
// a [26]int64 of counts and the same workload.
package main

import (
	"fmt"
	"strings"
)

func sequences(counts *[26]int64) int64 {
	var total int64
	for letter := 0; letter < 26; letter++ {
		if counts[letter] > 0 {
			counts[letter]--
			total += 1 + sequences(counts)
			counts[letter]++
		}
	}
	return total
}

func numTilePossibilities(tiles string) int64 {
	var counts [26]int64
	for i := 0; i < len(tiles); i++ {
		counts[tiles[i]-'A']++
	}
	return sequences(&counts)
}

var seed int64 = 1079

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 200
	n := 200
	sets := make([]string, 0, n)
	for s := 0; s < n; s++ {
		d := nextRandom()%7 + 1
		alphabet := []byte{}
		for int64(len(alphabet)) < d {
			c := byte('A' + nextRandom()%26)
			if !strings.ContainsRune(string(alphabet), rune(c)) {
				alphabet = append(alphabet, c)
			}
		}
		var b strings.Builder
		for i := 0; i < 7; i++ {
			b.WriteByte(alphabet[nextRandom()%d])
		}
		sets = append(sets, b.String())
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for j := 0; j < n; j++ {
			count := numTilePossibilities(sets[(j*7+r)%n])
			total += count
			check = (check*31 + count) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d sets of 7 tiles: %d sequences, checksum %d\n", rounds, n, total, check)
}
