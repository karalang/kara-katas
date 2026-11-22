// LeetCode #2868: The Wording Game -- the bench, as wording.kara: 20
// deals of 10^5 words, each played 20 times by the table arm.
package main

import (
	"fmt"
	"sort"
)

func table(words []string) []int64 {
	top := make([]int64, 26)
	for i := range top {
		top[i] = -1
	}
	for i, w := range words {
		top[w[0]-'a'] = int64(i)
	}
	return top
}

func canAliceWin(a, b []string) bool {
	last := a[0]
	tops := [2][]int64{table(a), table(b)}
	hands := [2][]string{a, b}
	turn := 1
	for {
		c := int(last[0] - 'a')
		same := tops[turn][c]
		if same >= 0 && hands[turn][same] > last {
			last = hands[turn][same]
		} else if c < 25 && tops[turn][c+1] >= 0 {
			last = hands[turn][tops[turn][c+1]]
		} else {
			return turn == 1
		}
		turn = 1 - turn
	}
}

var seed int64 = 2868

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func deal(n, letters, longest int64) ([]string, []string) {
	words := make([]string, 0, n)
	for i := int64(0); i < n; i++ {
		ln := nextRandom()%longest + 1
		w := make([]byte, ln)
		for k := range w {
			w[k] = byte('a' + nextRandom()%letters)
		}
		words = append(words, string(w))
	}
	sort.Strings(words)
	m := 0
	for _, w := range words {
		if m == 0 || words[m-1] != w {
			words[m] = w
			m++
		}
	}
	words = words[:m]
	var a, b []string
	first := int(nextRandom() % int64(m))
	for i, w := range words {
		if i == first || (nextRandom()%2 == 0 && i != (first+1)%m) {
			a = append(a, w)
		} else {
			b = append(b, w)
		}
	}
	return a, b
}

func main() {
	const count, rounds, n = 20, 20, 100000
	as := make([][]string, count)
	bs := make([][]string, count)
	for c := 0; c < count; c++ {
		letters := int64(5)
		if c%2 == 0 {
			letters = 26
		}
		as[c], bs[c] = deal(n, letters, 8)
	}
	var wins, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			win := canAliceWin(as[c], bs[c])
			w := int64(0)
			if win {
				wins++
				w = 1
			}
			check = (check*2 + r + w) % 1000000007
		}
	}
	fmt.Printf("%d deals of %d words, %d rounds: Alice wins %d, checksum %d\n", count, n, rounds, wins, check)
}
