// LeetCode #1554: Strings Differ by One Character -- bench: the ★ arm
// (every word entered once per place with that place blotted out) over 20
// lists of 1000 random words of 100 letters, built once, half of them with
// a pair planted that differs in one place, each asked 3 times. Go mirror of differ.kara.
package main

import "fmt"

func differByOne(dict []string) bool {
	seen := map[string]struct{}{}
	for _, word := range dict {
		letters := []rune(word)
		for j := range letters {
			blotted := make([]rune, len(letters))
			copy(blotted, letters)
			blotted[j] = '*'
			pattern := string(blotted)
			if _, ok := seen[pattern]; ok {
				return true
			}
			seen[pattern] = struct{}{}
		}
	}
	return false
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	alphabet := []rune("abcdefghijklmnopqrstuvwxyz")
	seed := int64(1554)
	lists := [][]string{}
	for l := 0; l < 20; l++ {
		dict := []string{}
		for w := 0; w < 1000; w++ {
			word := make([]rune, 100)
			for i := range word {
				word[i] = alphabet[nextRandom(&seed)%26]
			}
			dict = append(dict, string(word))
		}
		if l%2 == 1 {
			at := nextRandom(&seed) % 1000
			place := nextRandom(&seed) % 100
			letters := []rune(dict[at])
			if letters[place] == 'a' {
				letters[place] = 'b'
			} else {
				letters[place] = 'a'
			}
			twin := nextRandom(&seed) % 1000
			dict[twin] = string(letters)
		}
		lists = append(lists, dict)
	}
	yes, check := int64(0), int64(0)
	for pass := int64(0); pass < 3; pass++ {
		for l := range lists {
			if differByOne(lists[l]) {
				yes++
				check = mix(check, pass*20+int64(l))
			}
		}
	}
	fmt.Printf("3 passes over 20 lists of 1000 words of 100 letters: %d true, checksum %d\n", yes, check)
}
