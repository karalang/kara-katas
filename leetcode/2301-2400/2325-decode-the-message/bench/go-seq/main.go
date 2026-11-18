// LeetCode #2325: Decode the Message -- the bench, the ★ arm in Go. One
// walk over the key's bytes fills a table of 26, each letter's first
// appearance given the next letter of the alphabet, and the message is
// read through it, spaces kept. O(|key| + |message|).
package main

import (
	"fmt"
	"strings"
)

func decodeMessage(key, message string) string {
	var table [26]byte
	next := byte('a')
	for i := 0; i < len(key); i++ {
		b := key[i]
		if b != ' ' && table[b-'a'] == 0 {
			table[b-'a'] = next
			next++
		}
	}
	var decoded strings.Builder
	for i := 0; i < len(message); i++ {
		b := message[i]
		if b == ' ' {
			decoded.WriteByte(' ')
		} else {
			decoded.WriteByte(table[b-'a'])
		}
	}
	return decoded.String()
}

var seed int64 = 2325

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func letter() byte {
	roll := nextRandom() % 27
	if roll == 26 {
		return ' '
	}
	return byte('a' + roll)
}

func main() {
	keys := make([]string, 100)
	messages := make([]string, 100)
	for k := 0; k < 100; k++ {
		key := make([]byte, 0, 2000)
		for i := 0; i < 1974; i++ {
			key = append(key, letter())
		}
		keys[k] = string(key) + "abcdefghijklmnopqrstuvwxyz"
		message := make([]byte, 0, 2000)
		for i := 0; i < 2000; i++ {
			message = append(message, letter())
		}
		messages[k] = string(message)
	}
	var check int64
	for p := 0; p < 1000; p++ {
		for k := 0; k < 100; k++ {
			decoded := decodeMessage(keys[k], messages[k])
			check = (check*31 + int64(decoded[p%2000]) + int64(decoded[(7*p+k)%2000])) % 1000000007
			keys[k] = keys[k][1:] + keys[k][:1]
		}
	}
	fmt.Printf("1000 passes over 100 keys and messages of 2000: checksum %d\n", check)
}
