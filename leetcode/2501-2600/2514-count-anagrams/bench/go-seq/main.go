// LeetCode #2514: Count Anagrams -- Go mirror of the benchmark
// (anagrams.kara): the same sentences, passes, order and checksum.
package main

import (
	"fmt"
	"strings"
)

const MOD = 1000000007

func power(base, exponent int64) int64 {
	result, b, e := int64(1), base%MOD, exponent
	for e > 0 {
		if e%2 == 1 {
			result = result * b % MOD
		}
		b = b * b % MOD
		e /= 2
	}
	return result
}

func countAnagrams(s string) int64 {
	factorial := make([]int64, len(s)+1)
	factorial[0] = 1
	for i := 1; i <= len(s); i++ {
		factorial[i] = factorial[i-1] * int64(i) % MOD
	}
	answer := int64(1)
	for _, word := range strings.Split(s, " ") {
		counts := make([]int, 26)
		for i := 0; i < len(word); i++ {
			counts[word[i]-'a']++
		}
		answer = answer * factorial[len(word)] % MOD
		for _, c := range counts {
			answer = answer * power(factorial[c], MOD-2) % MOD
		}
	}
	return answer
}

var seed int64 = 2514

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	sentences := make([]string, 0, 20)
	for t := 0; t < 20; t++ {
		var text []byte
		for {
			length := nextRandom()%200 + 1
			if int64(len(text))+1+length > 100000 {
				break
			}
			if len(text) > 0 {
				text = append(text, ' ')
			}
			for k := int64(0); k < length; k++ {
				text = append(text, byte('a'+nextRandom()%26))
			}
		}
		sentences = append(sentences, string(text))
	}
	const passes = 4
	var check int64
	for p := int64(0); p < passes; p++ {
		start := check % 20
		for k := int64(0); k < 20; k++ {
			check = (check*31 + countAnagrams(sentences[(start+k)%20]) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 20 sentences of 10^5: checksum %d\n", passes, check)
}
