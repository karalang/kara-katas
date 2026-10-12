// Benchmark for #408: mirror of valid_word_abbreviation.kara (two
// pointers).
package main

import (
	"fmt"
	"os"
	"strconv"
)

func validWordAbbreviation(word, abbr string) bool {
	w := word
	a := abbr
	i, j := 0, 0
	for i < len(w) && j < len(a) {
		if a[j] >= 48 && a[j] <= 57 {
			if a[j] == 48 {
				return false
			}
			skip := 0
			for j < len(a) && a[j] >= 48 && a[j] <= 57 {
				skip = skip*10 + int(a[j]-48)
				j++
			}
			i += skip
		} else {
			if w[i] != a[j] {
				return false
			}
			i++
			j++
		}
	}
	return i == len(w) && j == len(a)
}

var seed int64 = 408

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 20000
	if len(os.Args) > 1 {
		count, _ = strconv.Atoi(os.Args[1])
	}
	rounds := 1000
	var n int64 = 20
	words := make([]string, 0, count)
	abbrs := make([]string, 0, count)
	for t := 0; t < count; t++ {
		w := make([]byte, n)
		for i := range w {
			w[i] = byte(97 + step()%2)
		}
		abbr := []byte{}
		var i int64
		number := false
		for i < n {
			if number || step()%2 == 0 {
				abbr = append(abbr, w[i])
				i++
				number = false
			} else {
				run := 1 + step()%(n-i)
				abbr = append(abbr, strconv.FormatInt(run, 10)...)
				i += run
				number = true
			}
		}
		words = append(words, string(w))
		abbrs = append(abbrs, string(abbr))
	}
	var valid, checksum int64
	for r := 0; r < rounds; r++ {
		var found int64
		for i := 0; i < count; i++ {
			if validWordAbbreviation(words[i], abbrs[(i+r)%count]) {
				found++
			}
		}
		valid += found
		checksum = (checksum*31 + found) % 1000000007
	}
	fmt.Printf("%d words, %d rounds: %d valid, checksum %d\n", count, rounds, valid, checksum)
}
