// LeetCode #2423: Remove Letter To Equalize Frequency -- the bench, the ★
// arm: the 26 letter counts, each held letter taken away once in turn and
// the counts left that are not zero compared.
package main

import "fmt"

var seed int64 = 2423

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func equalFrequency(word []byte) bool {
	var count [26]int64
	for _, b := range word {
		count[b-'a']++
	}
	for c := 0; c < 26; c++ {
		if count[c] == 0 {
			continue
		}
		count[c]--
		want := int64(0)
		equal := true
		for k := 0; k < 26; k++ {
			if count[k] > 0 {
				if want == 0 {
					want = count[k]
				} else if count[k] != want {
					equal = false
				}
			}
		}
		count[c]++
		if equal {
			return true
		}
	}
	return false
}

func main() {
	words := make([][]byte, 0, 10000)
	for w := 0; w < 10000; w++ {
		kinds := 1 + nextRandom()%20
		times := 1 + nextRandom()%5
		bytes := []byte{}
		for k := int64(0); k < kinds; k++ {
			for t := int64(0); t < times; t++ {
				bytes = append(bytes, byte('a'+k))
			}
		}
		if nextRandom()%2 == 0 {
			bytes = append(bytes, byte('a'+nextRandom()%26))
		} else {
			at := nextRandom() % int64(len(bytes))
			bytes = append(bytes[:at], bytes[at+1:]...)
		}
		for i := len(bytes) - 1; i >= 1; i-- {
			j := nextRandom() % int64(i+1)
			bytes[i], bytes[j] = bytes[j], bytes[i]
		}
		for len(bytes) < 2 {
			bytes = append(bytes, 'a')
		}
		words = append(words, bytes)
	}
	check := int64(0)
	for p := int64(0); p < 200; p++ {
		for _, w := range words {
			a := int64(0)
			if equalFrequency(w) {
				a = 1
			}
			check = (check*3 + a + p) % 1000000007
		}
	}
	fmt.Printf("200 passes over 10^4 words: checksum %d\n", check)
}
