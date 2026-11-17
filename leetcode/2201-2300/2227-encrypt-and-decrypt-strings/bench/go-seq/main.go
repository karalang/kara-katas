// LeetCode #2227: Encrypt and Decrypt Strings -- the benchmark's Go
// mirror of encrypter.kara: a map of values and a map counting the
// dictionary's encryptions.
package main

import (
	"fmt"
	"strings"
)

type Encrypter struct {
	table  map[rune]string
	counts map[string]int64
}

func newEncrypter(keys []rune, values []string, dictionary []string) *Encrypter {
	e := &Encrypter{table: map[rune]string{}, counts: map[string]int64{}}
	for i := range keys {
		e.table[keys[i]] = values[i]
	}
	for _, word := range dictionary {
		secret := e.encrypt(word)
		if secret != "" {
			e.counts[secret]++
		}
	}
	return e
}

func (e *Encrypter) encrypt(word1 string) string {
	var secret strings.Builder
	for _, c := range word1 {
		value, ok := e.table[c]
		if !ok {
			return ""
		}
		secret.WriteString(value)
	}
	return secret.String()
}

func (e *Encrypter) decrypt(word2 string) int64 {
	return e.counts[word2]
}

var seed int64 = 2227

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func drawWord(length, letters int64) string {
	b := make([]byte, length)
	for i := range b {
		b[i] = byte(97 + nextRandom()%letters)
	}
	return string(b)
}

func main() {
	keys := []rune{}
	values := []string{}
	for i := 0; i < 26; i++ {
		keys = append(keys, rune(97+i))
		values = append(values, drawWord(2, 3))
	}
	dictionary := make([]string, 100)
	for i := range dictionary {
		dictionary[i] = drawWord(100, 26)
	}
	words := make([]string, 200)
	for i := 0; i < 200; i++ {
		if i%2 == 0 {
			words[i] = drawWord(nextRandom()%2000+1, 26)
		} else if i%4 == 1 {
			var secret strings.Builder
			for _, c := range dictionary[nextRandom()%100] {
				secret.WriteString(values[c-97])
			}
			words[i] = secret.String()
		} else {
			words[i] = drawWord(200, 3)
		}
	}
	var check int64
	for r := 0; r < 500; r++ {
		// punch: one dictionary word drawn again before each round
		at := nextRandom() % 100
		dictionary[at] = drawWord(100, 26)
		e := newEncrypter(keys, values, dictionary)
		for i := 0; i < 200; i++ {
			if i%2 == 0 {
				secret := e.encrypt(words[i])
				check = (check*31 + int64(len(secret)) + int64(secret[len(secret)/2])) % 1000000007
			} else {
				check = (check*31 + e.decrypt(words[i])) % 1000000007
			}
		}
	}
	fmt.Printf("500 rounds of 200 calls: checksum %d\n", check)
}
