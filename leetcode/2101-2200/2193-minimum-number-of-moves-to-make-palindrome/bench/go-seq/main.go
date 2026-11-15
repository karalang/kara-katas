// benchmark's Go mirror of moves.kara (LeetCode #2193, the ★ arm): the
// twin swapped out to the end, over a copy of the word's bytes.
package main

import "fmt"

func minMoves(s string) int64 {
	b := []byte(s)
	left, right := 0, len(b)-1
	var moves int64
	for left < right {
		k := right
		for k > left && b[k] != b[left] {
			k--
		}
		if k == left {
			b[left], b[left+1] = b[left+1], b[left]
			moves++
			continue
		}
		for k < right {
			b[k], b[k+1] = b[k+1], b[k]
			k++
			moves++
		}
		left++
		right--
	}
	return moves
}

var seed int64 = 2193

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord() string {
	chars := make([]byte, 0, 2000)
	for i := 0; i < 1000; i++ {
		c := byte(97 + nextRandom()%26)
		chars = append(chars, c, c)
	}
	for i := 1999; i >= 1; i-- {
		j := nextRandom() % int64(i+1)
		chars[i], chars[j] = chars[j], chars[i]
	}
	return string(chars)
}

func main() {
	words := make([]string, 20)
	for w := range words {
		words[w] = randomWord()
	}
	var check int64
	for r := 0; r < 3000; r++ {
		check = (check*31 + minMoves(words[r%20])) % 1000000007
	}
	fmt.Printf("3000 solves: checksum %d\n", check)
}
