// Benchmark for #567: Go mirror of the ★ arm (a sliding window); see
// check_inclusion.kara.
package main

import "fmt"

func checkInclusion(s1, s2 string) bool {
	a := []rune(s1)
	b := []rune(s2)
	k := len(a)
	if k > len(b) {
		return false
	}
	need := make([]int64, 26)
	for _, c := range a {
		need[c-'a'] += 1
	}
	missing := int64(k)
	for i := 0; i < len(b); i++ {
		enter := b[i] - 'a'
		if need[enter] > 0 {
			missing -= 1
		}
		need[enter] -= 1
		if i >= k {
			leave := b[i-k] - 'a'
			need[leave] += 1
			if need[leave] > 0 {
				missing += 1
			}
		}
		if missing == 0 {
			return true
		}
	}
	return false
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomText(length, letters int64, seed *int64) string {
	alphabet := []rune("abcdefghijklmnopqrstuvwxyz")
	s := make([]rune, 0, length)
	for i := int64(0); i < length; i++ {
		s = append(s, alphabet[step(seed)%letters])
	}
	return string(s)
}

func main() {
	var count int64 = 100
	var rounds int64 = 300
	var seed int64 = 567
	s1s := make([]string, 0, count)
	s2s := make([]string, 0, count)
	for g := int64(0); g < count; g++ {
		letters := 3 + step(&seed)%24
		len1 := 5 + step(&seed)%196
		s1 := randomText(len1, letters, &seed)
		s2 := randomText(10000, letters, &seed)
		if g%2 == 0 {
			shuffled := []rune(s1)
			i := int64(len(shuffled)) - 1
			for i > 0 {
				j := step(&seed) % (i + 1)
				shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
				i -= 1
			}
			cut := step(&seed) % (10001 - int64(len(s1)))
			s2 = s2[:cut] + string(shuffled) + s2[cut+int64(len(s1)):]
		}
		s1s = append(s1s, s1)
		s2s = append(s2s, s2)
	}
	var found int64 = 0
	var checksum int64 = 0
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			p := (round*7 + g) % count
			got := checkInclusion(s1s[p], s2s[p])
			if got {
				found += 1
			}
			add := int64(1)
			if got {
				add = g + 2
			}
			checksum = (checksum*31 + add) % 1000000007
		}
	}
	fmt.Printf("%d pairs, %d rounds: %d found, checksum %d\n", count, rounds, found, checksum)
}
