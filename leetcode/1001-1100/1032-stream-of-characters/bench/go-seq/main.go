// LeetCode #1032: Stream of Characters -- bench
// Mirrors ../stream_checker.kara; see ../../README.md § Benchmarks.

package main

import "fmt"

type StreamChecker struct {
	next   [][]int64
	end    []bool
	stream []int64
}

func newRow() []int64 {
	row := make([]int64, 26)
	for k := range row {
		row[k] = -1
	}
	return row
}

func NewStreamChecker(words []string) *StreamChecker {
	next := [][]int64{newRow()}
	end := []bool{false}
	for _, word := range words {
		node := int64(0)
		for i := len(word) - 1; i >= 0; i-- {
			k := int64(word[i] - 'a')
			if next[node][k] == -1 {
				next[node][k] = int64(len(next))
				next = append(next, newRow())
				end = append(end, false)
			}
			node = next[node][k]
		}
		end[node] = true
	}
	return &StreamChecker{next: next, end: end}
}

func (s *StreamChecker) Query(letter byte) bool {
	s.stream = append(s.stream, int64(letter-'a'))
	node := int64(0)
	for i := len(s.stream) - 1; i >= 0; i-- {
		node = s.next[node][s.stream[i]]
		if node == -1 {
			return false
		}
		if s.end[node] {
			return true
		}
	}
	return false
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomText(seed *int64, n int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte(97 + nextRandom(seed)%2)
	}
	return string(b)
}

func main() {
	const rounds = 50
	seed := int64(1032)
	words := []string{}
	for w := 0; w < 2000; w++ {
		n := 50 + nextRandom(&seed)%151
		words = append(words, randomText(&seed, n))
	}
	stream := randomText(&seed, 40000)
	var found, check int64
	for r := 0; r < rounds; r++ {
		checker := NewStreamChecker(append([]string(nil), words...))
		for i := 0; i < len(stream); i++ {
			var hit int64
			if checker.Query(stream[i]) {
				hit = 1
			}
			found += hit
			check = (check*3 + hit + 1) % 1000000007
		}
	}
	fmt.Printf("2000 words, 40000 queries, %d rounds: %d found, checksum %d\n", rounds, found, check)
}
