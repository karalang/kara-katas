// Benchmark for #438: mirror of find_anagrams.kara (a sliding window of
// letter counts) on 40 patterns searched in one random text of
// 1,000,000 letters.
package main

import (
	"fmt"
	"strings"
)

func findAnagrams(s, p string) []int64 {
	n, m := len(s), len(p)
	starts := []int64{}
	if m > n {
		return starts
	}
	// need[c] is p's count of c minus the window's.
	var need [26]int64
	for i := 0; i < m; i++ {
		need[p[i]-'a']++
	}
	differ := 0
	for c := 0; c < 26; c++ {
		if need[c] != 0 {
			differ++
		}
	}
	for i := 0; i < n; i++ {
		enter := s[i] - 'a'
		if need[enter] == 0 {
			differ++
		}
		need[enter]--
		if need[enter] == 0 {
			differ--
		}
		if i >= m {
			leave := s[i-m] - 'a'
			if need[leave] == 0 {
				differ++
			}
			need[leave]++
			if need[leave] == 0 {
				differ--
			}
		}
		if i >= m-1 && differ == 0 {
			starts = append(starts, int64(i-m+1))
		}
	}
	return starts
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const size, patterns = 1000000, 40
	seed := int64(438)
	// Letters from 'a' to 'd', so that short patterns have many
	// anagrams in the text.
	var b strings.Builder
	for i := 0; i < size; i++ {
		b.WriteByte(byte('a' + nextRandom(&seed)%4))
	}
	text := b.String()
	var found, checksum int64
	for q := 0; q < patterns; q++ {
		length := 1 + nextRandom(&seed)%12
		var pb strings.Builder
		for i := int64(0); i < length; i++ {
			pb.WriteByte(byte('a' + nextRandom(&seed)%4))
		}
		starts := findAnagrams(text, pb.String())
		found += int64(len(starts))
		for _, i := range starts {
			checksum = (checksum*31 + i) % 1000000007
		}
	}
	fmt.Printf("%d patterns in a text of %d: %d anagrams, checksum %d\n", patterns, size, found, checksum)
}
