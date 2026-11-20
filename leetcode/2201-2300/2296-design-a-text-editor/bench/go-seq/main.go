// LeetCode #2296: Design a Text Editor -- the bench, the ★ arm in Go. Two
// stacks of letters: `left` holds the text before the cursor in order,
// `right` the text after it reversed.
package main

import (
	"fmt"
	"strconv"
)

type TextEditor struct {
	left, right []byte
}

func (e *TextEditor) addText(text string) {
	for i := 0; i < len(text); i++ {
		e.left = append(e.left, text[i])
	}
}

func (e *TextEditor) deleteText(k int64) int64 {
	n := min(k, int64(len(e.left)))
	e.left = e.left[:int64(len(e.left))-n]
	return n
}

func (e *TextEditor) cursorLeft(k int64) string {
	for i := int64(0); i < k && len(e.left) > 0; i++ {
		e.right = append(e.right, e.left[len(e.left)-1])
		e.left = e.left[:len(e.left)-1]
	}
	return e.tail()
}

func (e *TextEditor) cursorRight(k int64) string {
	for i := int64(0); i < k && len(e.right) > 0; i++ {
		e.left = append(e.left, e.right[len(e.right)-1])
		e.right = e.right[:len(e.right)-1]
	}
	return e.tail()
}

func (e *TextEditor) tail() string {
	return string(e.left[len(e.left)-min(len(e.left), 10):])
}

type call struct {
	kind, k int64
	text    string
}

var seed int64 = 2296

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func callsOf(count int) []call {
	calls := make([]call, 0, count)
	for i := 0; i < count; i++ {
		kind := nextRandom() % 4
		k := nextRandom()%40 + 1
		text := []byte{}
		if kind == 0 {
			for j := int64(0); j < k; j++ {
				text = append(text, byte('a'+nextRandom()%26))
			}
		}
		calls = append(calls, call{kind, k, string(text)})
	}
	return calls
}

func run(calls []call) []string {
	e := &TextEditor{}
	var answers []string
	for _, c := range calls {
		switch c.kind {
		case 0:
			e.addText(c.text)
		case 1:
			answers = append(answers, strconv.FormatInt(e.deleteText(c.k), 10))
		case 2:
			answers = append(answers, e.cursorLeft(c.k))
		default:
			answers = append(answers, e.cursorRight(c.k))
		}
	}
	return answers
}

func main() {
	var editors [][]call
	for i := 0; i < 10; i++ {
		editors = append(editors, callsOf(20000))
	}
	var check int64
	for pass := 0; pass < 10; pass++ {
		for _, calls := range editors {
			for _, answer := range run(calls) {
				for i := 0; i < len(answer); i++ {
					check = (check*131 + int64(answer[i])) % 1000000007
				}
				check = (check*131 + 1) % 1000000007
			}
		}
	}
	fmt.Printf("10 passes over 10 editors of 2 * 10^4 calls: checksum %d\n", check)
}
