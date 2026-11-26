// LeetCode #1781: Sum of Beauty of All Substrings -- the bench in Go,
// mirroring beauty_sum.kara: the letters' counts grown from each start.
package main

import "fmt"

func beautySum(s []rune) int32 {
	n := len(s)
	var total int32
	for i := 0; i < n; i++ {
		var counts [26]int32
		for j := i; j < n; j++ {
			counts[s[j]-'a']++
			var most int32
			fewest := int64(n)
			for _, c := range counts {
				if c > 0 {
					if c > most {
						most = c
					}
					if int64(c) < fewest {
						fewest = int64(c)
					}
				}
			}
			total += int32(int64(most) - fewest)
		}
	}
	return total
}

var seed int64 = 1781

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	words := make([][]rune, 0, 48)
	for w := int64(0); w < 48; w++ {
		letters := 2 + w%12*2
		s := make([]rune, 0, 500)
		for k := 0; k < 500; k++ {
			s = append(s, rune(97+nextRandom()%letters))
		}
		words = append(words, s)
	}
	var check int64
	for w := 0; w < 48; w++ {
		check = (check*31 + int64(beautySum(words[w]))) % 1000000007
	}
	fmt.Printf("48 strings of 500 letters: checksum %d\n", check)
}
