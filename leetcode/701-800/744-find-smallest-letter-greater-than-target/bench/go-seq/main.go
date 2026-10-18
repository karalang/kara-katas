// LeetCode 744 — Find Smallest Letter Greater Than Target, bench: the ★
// arm (binary search) on lists of 10000 sorted letters, many random
// targets each. Mirrors next_greatest_letter.kara.
package main

import "fmt"

func nextGreatestLetter(letters []rune, target rune) rune {
	lo, hi := 0, len(letters)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if letters[mid] <= target {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	if lo == len(letters) {
		return letters[0]
	}
	return letters[lo]
}

var seed int64 = 744

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 60
	n := 10000
	queries := 100000
	a := int64('a')
	z := int64('z')
	var total int64
	for r := 0; r < rounds; r++ {
		letters := make([]rune, 0)
		c := a + nextRandom()%6
		for i := 0; i < n; i++ {
			if nextRandom()%500 == 0 && c < z {
				c++
			}
			letters = append(letters, rune(c))
		}
		if letters[0] == letters[n-1] {
			letters[n-1] = letters[0] + 1
		}
		for q := 0; q < queries; q++ {
			target := rune(a + nextRandom()%26)
			total += int64(nextGreatestLetter(letters, target))
		}
	}
	fmt.Printf("%d rounds of 100000 queries on 10000 letters: answers sum to %d\n", rounds, total)
}
