// LeetCode #1309 bench in Go: the ★ arm (the code read from the right, a `#`
// taking the two digits before it) on the same 200 codes and 500 passes.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func freqAlphabets(s string) string {
	var letters []byte
	i := len(s) - 1
	for i >= 0 {
		var number byte
		if s[i] == '#' {
			i -= 3
			number = (s[i+1]-'0')*10 + (s[i+2] - '0')
		} else {
			i--
			number = s[i+1] - '0'
		}
		letters = append(letters, 'a'+number-1)
	}
	for a, b := 0, len(letters)-1; a < b; a, b = a+1, b-1 {
		letters[a], letters[b] = letters[b], letters[a]
	}
	return string(letters)
}

var seed int64 = 1309

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func encode(letters []int64) string {
	var code strings.Builder
	for _, k := range letters {
		code.WriteString(strconv.FormatInt(k+1, 10))
		if k >= 9 {
			code.WriteByte('#')
		}
	}
	return code.String()
}

func main() {
	texts := make([][]int64, 200)
	codes := make([]string, 200)
	for t := range texts {
		letters := make([]int64, 300)
		for k := range letters {
			letters[k] = nextRandom() % 26
		}
		codes[t] = encode(letters)
		texts[t] = letters
	}
	var check int64
	for pass := int64(0); pass < 500; pass++ {
		t := check % 200
		texts[t][(check/200)%300] = (check / 7) % 26
		codes[t] = encode(texts[t])
		for c := 0; c < 200; c++ {
			got := freqAlphabets(codes[c])
			check = (check*31 + int64(got[check%int64(len(got))]) + int64(len(got)) + pass) % 1000000007
		}
	}
	fmt.Printf("500 passes over 200 codes: checksum %d\n", check)
}
