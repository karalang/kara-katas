// LeetCode #2288: Apply Discount to Prices -- the bench, the ★ arm in Go.
// Split on spaces; a `$` and then only digits is a price, discounted in
// whole cents and written back with two decimals.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func isPrice(word string) bool {
	if len(word) < 2 || word[0] != '$' {
		return false
	}
	for i := 1; i < len(word); i++ {
		if word[i] < '0' || word[i] > '9' {
			return false
		}
	}
	return true
}

func discountPrices(sentence string, discount int64) string {
	words := []string{}
	for _, word := range strings.Split(sentence, " ") {
		if isPrice(word) {
			price, _ := strconv.ParseInt(word[1:], 10, 64)
			cents := price * (100 - discount)
			words = append(words, fmt.Sprintf("$%d.%02d", cents/100, cents%100))
		} else {
			words = append(words, word)
		}
	}
	return strings.Join(words, " ")
}

var seed int64 = 2288

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func word() string {
	kind := nextRandom() % 4
	length := nextRandom()%8 + 1
	var b strings.Builder
	if kind < 2 {
		b.WriteByte('$')
	}
	for i := int64(0); i < length; i++ {
		r := nextRandom()
		if kind == 0 || kind == 3 {
			b.WriteByte(byte('0' + r%10))
		} else {
			b.WriteByte(byte('a' + r%26))
		}
	}
	return b.String()
}

func main() {
	sentences := make([]string, 0, 4000)
	for k := 0; k < 4000; k++ {
		words := make([]string, 12)
		for i := range words {
			words[i] = word()
		}
		sentences = append(sentences, strings.Join(words, " "))
	}
	var check int64
	for pass := int64(0); pass < 50; pass++ {
		for _, sentence := range sentences {
			answer := discountPrices(sentence, pass*2)
			check = (check*31 + int64(len(answer)) + int64(answer[len(answer)-2])) % 1000000007
		}
	}
	fmt.Printf("50 passes over 4000 sentences: checksum %d\n", check)
}
