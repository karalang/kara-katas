// LeetCode #418: Sentence Screen Fitting -- Go mirror of
// sentence_screen.kara (one pointer into the text).
package main

import (
	"fmt"
	"strings"
)

func wordsTyping(sentence []string, rows, cols int64) int64 {
	text := strings.Join(sentence, " ") + " "
	length := int64(len(text))
	var at int64
	for r := int64(0); r < rows; r++ {
		at += cols
		if text[at%length] == ' ' {
			at++
		} else {
			for at > 0 && text[(at-1)%length] != ' ' {
				at--
			}
		}
	}
	return at / length
}

var seed int64 = 418

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	calls := 10000
	pool := make([]string, 0, 200)
	for i := 0; i < 200; i++ {
		length := 1 + step()%10
		var b strings.Builder
		for j := int64(0); j < length; j++ {
			b.WriteByte(byte(97 + step()%26))
		}
		pool = append(pool, b.String())
	}
	var total, checksum int64
	for c := 0; c < calls; c++ {
		n := 1 + step()%100
		sentence := make([]string, 0, n)
		for i := int64(0); i < n; i++ {
			sentence = append(sentence, pool[step()%200])
		}
		rows := 1 + step()%20000
		cols := 10 + step()%19991
		answer := wordsTyping(sentence, rows, cols)
		total += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d calls: total %d, checksum %d\n", calls, total, checksum)
}
