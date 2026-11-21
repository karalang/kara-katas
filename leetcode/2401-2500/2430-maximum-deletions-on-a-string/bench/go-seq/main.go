// LeetCode #2430: Maximum Deletions on a String -- the bench, the ★ arm:
// the longest common prefix of the suffixes at `i` and `k` kept in two
// rows, each row from the one after it, and `best[i]` the most
// operations that clear the suffix from `i`.
package main

import "fmt"

func deleteString(b []byte) int64 {
	n := len(b)
	nextRow := make([]int64, n+1)
	row := make([]int64, n+1)
	best := make([]int64, n+1)
	for i := n - 1; i >= 0; i-- {
		for k := i + 1; k < n; k++ {
			if b[i] == b[k] {
				row[k] = nextRow[k+1] + 1
			} else {
				row[k] = 0
			}
		}
		best[i] = 1
		for j := 1; j < (n-i)/2+1; j++ {
			if row[i+j] >= int64(j) && best[i+j]+1 > best[i] {
				best[i] = best[i+j] + 1
			}
		}
		nextRow, row = row, nextRow
	}
	return best[0]
}

var seed int64 = 2430

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var words [][]byte
	for w := 0; w < 8; w++ {
		var word []byte
		for i := int64(0); i < 4000; i++ {
			back := 1 + nextRandom()%3
			if i >= back && nextRandom()%2 == 0 {
				word = append(word, word[i-back])
			} else {
				word = append(word, byte('a'+nextRandom()%2))
			}
		}
		words = append(words, word)
	}
	var check int64
	for p := int64(0); p < 6; p++ {
		for w := range words {
			at := (p*997 + int64(w)*131) % 4000
			words[w][at] = byte('a' + p%2)
			check = (check*31 + deleteString(words[w]) + p) % 1000000007
		}
	}
	fmt.Printf("6 passes over 8 words of 4000 letters: checksum %d\n", check)
}
