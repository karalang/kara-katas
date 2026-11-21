// LeetCode #2468: Split Message Based on Limit -- the bench, the ★ arm in
// Go: the least part count found with a running sum of the counts'
// digits, each count's digits by `strconv.Itoa`, then the parts cut in
// order and joined by string concatenation.
package main

import (
	"fmt"
	"strconv"
)

func digits(v int64) int64 {
	return int64(len(strconv.FormatInt(v, 10)))
}

func splitMessage(message string, limit int64) []string {
	n := int64(len(message))
	var digitSum, parts int64
	for b := int64(1); 3+2*digits(b) < limit; b++ {
		digitSum += digits(b)
		if b*(limit-3-digits(b))-digitSum >= n {
			parts = b
			break
		}
	}
	out := []string{}
	if parts == 0 {
		return out
	}
	var at int64
	for a := int64(1); a <= parts; a++ {
		room := limit - 3 - digits(a) - digits(parts)
		end := min(at+room, n)
		out = append(out, message[at:end]+"<"+strconv.FormatInt(a, 10)+"/"+strconv.FormatInt(parts, 10)+">")
		at = end
	}
	return out
}

var seed int64 = 2468

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 messages of 10^4 lowercase letters and spaces built once; then
	// 2600 passes, each choosing every message's limit, from 12 to 211,
	// from the checksum so far, then splitting it and folding the part
	// count, the last part's length and the pass into the checksum
	letters := "abcdefghijklmnopqrstuvwxyz "
	messages := []string{}
	for m := 0; m < 20; m++ {
		text := make([]byte, 10000)
		for i := range text {
			text[i] = letters[nextRandom()%27]
		}
		messages = append(messages, string(text))
	}
	var check int64
	for p := int64(0); p < 2600; p++ {
		for _, m := range messages {
			limit := 12 + check%200
			parts := splitMessage(m, limit)
			last := int64(len(parts[len(parts)-1]))
			check = (check*31 + int64(len(parts)) + last + p) % 1000000007
		}
	}
	fmt.Printf("2600 passes over 20 messages of 10^4: checksum %d\n", check)
}
