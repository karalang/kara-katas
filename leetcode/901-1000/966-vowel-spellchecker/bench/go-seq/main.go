// Benchmark: LeetCode #966 Vowel Spellchecker -- the ★ arm, three maps,
// on cases of 5000 words and 5000 queries, LeetCode's largest. Mirrors
// spellchecker.kara, .c, .rs and .py.
package main

import (
	"fmt"
	"strings"
)

func devowel(w string) string {
	var b strings.Builder
	for _, c := range strings.ToLower(w) {
		if strings.ContainsRune("aeiou", c) {
			b.WriteByte('*')
		} else {
			b.WriteRune(c)
		}
	}
	return b.String()
}

func spellchecker(wordlist, queries []string) []string {
	exact := map[string]bool{}
	byCase := map[string]string{}
	byVowel := map[string]string{}
	for _, w := range wordlist {
		exact[w] = true
		if _, ok := byCase[strings.ToLower(w)]; !ok {
			byCase[strings.ToLower(w)] = w
		}
		if _, ok := byVowel[devowel(w)]; !ok {
			byVowel[devowel(w)] = w
		}
	}
	out := make([]string, 0, len(queries))
	for _, q := range queries {
		if exact[q] {
			out = append(out, q)
		} else if w, ok := byCase[strings.ToLower(q)]; ok {
			out = append(out, w)
		} else if w, ok := byVowel[devowel(q)]; ok {
			out = append(out, w)
		} else {
			out = append(out, "")
		}
	}
	return out
}

var seed int64 = 966

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

const alphabet = "aeioukbAEIOUKB"

func spell(letters []int64) string {
	b := make([]byte, len(letters))
	for i, x := range letters {
		b[i] = alphabet[x]
	}
	return string(b)
}

func randomWord(n int64) []int64 {
	w := make([]int64, n)
	for i := range w {
		w[i] = nextRandom() % 14
	}
	return w
}

func queryFrom(w []int64, kind, maxLen int64) []int64 {
	if kind == 3 {
		return randomWord(1 + nextRandom()%maxLen)
	}
	q := append([]int64(nil), w...)
	for i := range q {
		if kind == 1 && nextRandom()%2 == 0 {
			q[i] = (q[i] + 7) % 14
		} else if kind == 2 && q[i]%7 < 5 && nextRandom()%2 == 0 {
			a := nextRandom() % 5
			q[i] = a + 7*(nextRandom()%2)
		}
	}
	return q
}

func fold(s string, check int64) int64 {
	h := check
	for i := 0; i < len(s); i++ {
		h = (h*131 + int64(s[i])) % 1000000007
	}
	return (h*131 + 1) % 1000000007
}

func randomCase(n, m, maxLen int64) ([]string, []string) {
	ws := make([][]int64, n)
	for i := range ws {
		ws[i] = randomWord(1 + nextRandom()%maxLen)
	}
	qs := make([]string, m)
	for j := range qs {
		w := ws[nextRandom()%n]
		kind := nextRandom() % 4
		qs[j] = spell(queryFrom(w, kind, maxLen))
	}
	wl := make([]string, n)
	for i, w := range ws {
		wl[i] = spell(w)
	}
	return wl, qs
}

func main() {
	rounds := 200
	var wls, qss [][]string
	for c := 0; c < 5; c++ {
		wl, qs := randomCase(5000, 5000, 7)
		wls = append(wls, wl)
		qss = append(qss, qs)
	}
	var matched, check int64
	for r := 0; r < rounds; r++ {
		got := spellchecker(wls[r%5], qss[r%5])
		for _, g := range got {
			if len(g) > 0 {
				matched++
			}
			check = fold(g, check)
		}
	}
	fmt.Printf("%d rounds over 5 cases of 5000 words and 5000 queries: %d matched, checksum %d\n", rounds, matched, check)
}
