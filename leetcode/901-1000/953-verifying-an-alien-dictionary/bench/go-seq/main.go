// LeetCode #953: Verifying an Alien Dictionary -- Go mirror of the Kara
// bench program (a rank per letter).
package main

import "fmt"

func isAlienSorted(words []string, order string) bool {
	var rank [26]int64
	for i := 0; i < 26; i++ {
		rank[order[i]-'a'] = int64(i)
	}
	for w := 1; w < len(words); w++ {
		a := words[w-1]
		b := words[w]
		k := 0
		for k < len(a) && k < len(b) && a[k] == b[k] {
			k++
		}
		if k == len(b) {
			if k < len(a) {
				return false
			}
		} else if k < len(a) && rank[a[k]-'a'] > rank[b[k]-'a'] {
			return false
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func before(x, y string, rank *[26]int64) bool {
	k := 0
	for k < len(x) && k < len(y) && x[k] == y[k] {
		k++
	}
	if k == len(y) {
		return false
	} else if k == len(x) {
		return true
	}
	return rank[x[k]-'a'] < rank[y[k]-'a']
}

func main() {
	rounds, count, n := 2000, 200, 100
	seed := int64(953)
	orders := []string{}
	sets := [][]string{}
	for s := 0; s < count; s++ {
		letters := make([]byte, 26)
		for i := 0; i < 26; i++ {
			letters[i] = byte('a' + i)
		}
		for i := 0; i < 26; i++ {
			j := i + int(nextRandom(&seed)%int64(26-i))
			letters[i], letters[j] = letters[j], letters[i]
		}
		var rank [26]int64
		for i := 0; i < 26; i++ {
			rank[letters[i]-'a'] = int64(i)
		}
		order := string(letters)
		words := make([]string, 0, n)
		for i := 0; i < n; i++ {
			m := 1 + nextRandom(&seed)%20
			w := make([]byte, m)
			for c := int64(0); c < m; c++ {
				w[c] = letters[nextRandom(&seed)%3]
			}
			words = append(words, string(w))
		}
		for i := 1; i < n; i++ {
			j := i
			for j > 0 && before(words[j], words[j-1], &rank) {
				words[j], words[j-1] = words[j-1], words[j]
				j--
			}
		}
		if s%3 == 2 {
			words[n-2], words[n-1] = words[n-1], words[n-2]
		}
		orders = append(orders, order)
		sets = append(sets, words)
	}
	sorted, check := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			k := (r + i) % count
			ok := isAlienSorted(sets[k], orders[k])
			if ok {
				sorted++
			}
			v := int64(2)
			if ok {
				v = 1
			}
			check = (check*31 + v) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d sets of %d words: %d sorted, checksum %d\n", rounds, count, n, sorted, check)
}
