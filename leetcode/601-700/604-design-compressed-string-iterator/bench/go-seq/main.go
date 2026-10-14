// Benchmark for #604: Go mirror of the ★ arm (read as you go); see
// ../string_iterator.kara. The text is copied into a `[]rune`, as the
// Kāra arm collects it.
package main

import "fmt"

type StringIterator struct {
	text    []rune
	at      int
	current rune
	left    int64
}

func newStringIterator(compressed string) *StringIterator {
	return &StringIterator{text: []rune(compressed), current: ' '}
}

func (it *StringIterator) Next() rune {
	if it.left == 0 {
		if it.at == len(it.text) {
			return ' '
		}
		it.current = it.text[it.at]
		it.at++
		var count int64
		for it.at < len(it.text) && it.text[it.at] >= '0' && it.text[it.at] <= '9' {
			count = count*10 + int64(it.text[it.at]-48)
			it.at++
		}
		it.left = count
	}
	it.left--
	return it.current
}

func (it *StringIterator) HasNext() bool {
	return it.left > 0 || it.at < len(it.text)
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 1000
	rounds := 200
	seed := int64(604)
	texts := []string{}
	for t := 0; t < count; t++ {
		text := ""
		for {
			k := step(&seed) % 52
			var letter rune
			if k < 26 {
				letter = rune(65 + k)
			} else {
				letter = rune(97 + k - 26)
			}
			var n int64
			if step(&seed)%10 == 0 {
				hi := step(&seed)
				lo := step(&seed)
				n = 1 + (hi*32768+lo)%1000000000
			} else {
				n = 1 + step(&seed)%20
			}
			run := fmt.Sprintf("%c%d", letter, n)
			if len(text)+len(run) > 1000 {
				break
			}
			text += run
		}
		texts = append(texts, text)
	}
	total := 0
	var checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			it := newStringIterator(texts[(round*7+g)%count])
			for i := 0; i < 50; i++ {
				if it.HasNext() {
					total++
				}
				c := it.Next()
				checksum = (checksum*31 + int64(c)) % 1000000007
			}
		}
	}
	fmt.Printf("%d texts, %d rounds: %d letters left, checksum %d\n", count, rounds, total, checksum)
}
