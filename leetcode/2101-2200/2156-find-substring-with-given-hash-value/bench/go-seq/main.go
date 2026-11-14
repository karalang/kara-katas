// LeetCode #2156: Find Substring With Given Hash Value -- the benchmark's
// Go mirror of substring.kara.
package main

import "fmt"

func subStrHash(s string, power, modulo, k, hashValue int64) string {
	letters := make([]int64, len(s))
	for i := 0; i < len(s); i++ {
		letters[i] = int64(s[i]-'a') + 1
	}
	n := int64(len(letters))
	p := power % modulo
	top := 1 % modulo
	for j := int64(0); j < k; j++ {
		top = top * p % modulo
	}
	var hash int64
	start := n - k
	for i := n - 1; i >= 0; i-- {
		hash = (hash*p + letters[i]) % modulo
		if i+k < n {
			hash = (hash - letters[i+k]*top%modulo + modulo) % modulo
		}
		if i+k <= n && hash == hashValue {
			start = i
		}
	}
	return s[start : start+k]
}

var seed int64 = 2156

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func windowHash(s string, start, k, power, modulo int64) int64 {
	var hash int64
	weight := 1 % modulo
	for j := int64(0); j < k; j++ {
		hash = (hash + int64(s[start+j]-'a'+1)*weight) % modulo
		weight = weight * power % modulo
	}
	return hash
}

func main() {
	strings := make([][]byte, 4)
	for t := range strings {
		strings[t] = make([]byte, 20000)
		for i := range strings[t] {
			strings[t][i] = byte('a' + nextRandom()%26)
		}
	}
	var total, check int64
	for round := int64(0); round < 50; round++ {
		for t := 0; t < 4; t++ {
			at := nextRandom() % 20000
			strings[t][at] = byte('a' + nextRandom()%26)
			s := string(strings[t])
			k := nextRandom()%20000 + 1
			power := 1000000000 - nextRandom()
			modulo := 1000000000 - nextRandom()
			start := nextRandom() % (20000 - k + 1)
			hashValue := windowHash(s, start, k, power, modulo)
			found := subStrHash(s, power, modulo, k, hashValue)
			n := int64(len(found))
			total += n
			check = (check*31 + n + int64(found[0]) + int64(found[n-1]) + round) % 1000000007
		}
	}
	fmt.Printf("200 solves: %d letters in all, checksum %d\n", total, check)
}
