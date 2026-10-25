// Benchmark: LeetCode #1002 Find Common Characters -- the ★ arm, the
// least count of each letter, on lists of 100 words of 100 letters,
// LeetCode's largest. Mirrors common_chars.kara, .c, .rs and .py.
package main

import "fmt"

func commonChars(words []string) []string {
	least := make([]int64, 26)
	for i := range least {
		least[i] = 1000
	}
	for _, word := range words {
		count := make([]int64, 26)
		for _, c := range word {
			count[c-'a']++
		}
		for i := 0; i < 26; i++ {
			least[i] = min(least[i], count[i])
		}
	}
	ans := []string{}
	for i := 0; i < 26; i++ {
		for k := int64(0); k < least[i]; k++ {
			ans = append(ans, string(rune('a'+i)))
		}
	}
	return ans
}

var seed int64 = 1002

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 1000
	// 20 lists of 100 words of 100 letters, list t drawing its letters
	// from the first 2 + t % 10 of the alphabet
	lists := [][]string{}
	for t := 0; t < 20; t++ {
		alphabet := int64(2 + t%10)
		words := []string{}
		for w := 0; w < 100; w++ {
			word := []byte{}
			for k := 0; k < 100; k++ {
				word = append(word, byte(97+nextRandom()%alphabet))
			}
			words = append(words, string(word))
		}
		lists = append(lists, words)
	}
	var found, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			ans := commonChars(lists[(r+i)%20])
			found += int64(len(ans))
			for _, s := range ans {
				for _, c := range s {
					check = (check*31 + int64(c)) % 1000000007
				}
			}
		}
	}
	fmt.Printf("%d rounds over 20 lists of 100 words of 100 letters: %d common letters, checksum %d\n", rounds, found, check)
}
