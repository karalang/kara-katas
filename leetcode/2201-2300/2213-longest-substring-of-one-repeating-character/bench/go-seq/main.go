// LeetCode #2213: Longest Substring of One Repeating Character -- bench
// mirror of repeating.kara: a segment tree over the letters, each node
// keeping the longest run from its start, from its end and inside.
package main

import "fmt"

type tree struct {
	letters              []byte
	prefix, suffix, best []int64
}

func (t *tree) pull(node, lo, hi int) {
	mid := (lo + hi) / 2
	left, right := 2*node, 2*node+1
	joined := t.letters[mid] == t.letters[mid+1]
	if joined && t.prefix[left] == int64(mid-lo+1) {
		t.prefix[node] = t.prefix[left] + t.prefix[right]
	} else {
		t.prefix[node] = t.prefix[left]
	}
	if joined && t.suffix[right] == int64(hi-mid) {
		t.suffix[node] = t.suffix[right] + t.suffix[left]
	} else {
		t.suffix[node] = t.suffix[right]
	}
	t.best[node] = max(t.best[left], t.best[right])
	if joined {
		t.best[node] = max(t.best[node], t.suffix[left]+t.prefix[right])
	}
}

func (t *tree) build(node, lo, hi int) {
	if lo == hi {
		t.prefix[node], t.suffix[node], t.best[node] = 1, 1, 1
		return
	}
	mid := (lo + hi) / 2
	t.build(2*node, lo, mid)
	t.build(2*node+1, mid+1, hi)
	t.pull(node, lo, hi)
}

func (t *tree) update(node, lo, hi, at int) {
	if lo == hi {
		return
	}
	mid := (lo + hi) / 2
	if at <= mid {
		t.update(2*node, lo, mid, at)
	} else {
		t.update(2*node+1, mid+1, hi, at)
	}
	t.pull(node, lo, hi)
}

func longestRepeating(s, queryCharacters []byte, queryIndices []int) []int64 {
	n := len(s)
	t := &tree{append([]byte(nil), s...), make([]int64, 4*n), make([]int64, 4*n), make([]int64, 4*n)}
	t.build(1, 0, n-1)
	lengths := make([]int64, 0, len(queryIndices))
	for q, at := range queryIndices {
		t.letters[at] = queryCharacters[q]
		t.update(1, 0, n-1, at)
		lengths = append(lengths, t.best[1])
	}
	return lengths
}

var seed int64 = 2213

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n int, letters int64) []byte {
	w := make([]byte, n)
	for i := range w {
		w[i] = byte('a' + nextRandom()%letters)
	}
	return w
}

type word struct {
	s, qc []byte
	qi    []int
}

func main() {
	var words []word
	for w := 0; w < 6; w++ {
		// 10^5 letters from 2, 3 and 26 in turn, with 10^5 queries
		letters := []int64{2, 3, 26}[w%3]
		s := randomWord(100000, letters)
		qc := randomWord(100000, letters)
		qi := make([]int, 100000)
		for i := range qi {
			qi[i] = int(nextRandom() % 100000)
		}
		words = append(words, word{s, qc, qi})
	}
	var check int64
	for _, w := range words {
		for _, length := range longestRepeating(w.s, w.qc, w.qi) {
			check = (check*31 + length) % 1000000007
		}
	}
	fmt.Printf("6 words of 10^5: checksum %d\n", check)
}
