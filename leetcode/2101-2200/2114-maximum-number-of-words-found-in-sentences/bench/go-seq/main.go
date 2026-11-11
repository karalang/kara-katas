// LeetCode #2114: Maximum Number of Words Found in Sentences -- the
// benchmark, the same algorithm as words.kara: each sentence's spaces
// counted over its bytes, plus one, and the largest taken.

package main

import "fmt"

func mostWordsFound(sentences [][]byte) int64 {
	var most int64
	for _, s := range sentences {
		words := int64(1)
		for _, b := range s {
			if b == ' ' {
				words++
			}
		}
		if words > most {
			most = words
		}
	}
	return most
}

var seed int64 = 2114

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][][]byte, 200)
	for a := range lists {
		sentences := make([][]byte, 100)
		for i := range sentences {
			words := nextRandom()%25 + 1
			s := []byte{}
			for w := int64(0); w < words; w++ {
				if w > 0 {
					s = append(s, ' ')
				}
				n := nextRandom()%6 + 1
				for k := int64(0); k < n; k++ {
					s = append(s, byte('a'+nextRandom()%26))
				}
			}
			sentences[i] = s
		}
		lists[a] = sentences
	}
	var total, check int64
	for round := 0; round < 10; round++ {
		for a := 0; a < 200; a++ {
			j := (round*37 + a) % 100
			lists[a][j] = append(lists[a][j], ' ', 'a')
			got := mostWordsFound(lists[a])
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("2000 solves: %d words, checksum %d\n", total, check)
}
