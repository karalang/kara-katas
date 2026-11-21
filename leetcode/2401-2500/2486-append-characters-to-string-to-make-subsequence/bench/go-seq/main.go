// LeetCode #2486: Append Characters to String to Make Subsequence --
// bench, Go mirror of append.kara.
package main

import "fmt"

func appendCharacters(s, t string) int64 {
	wanted := []rune(t)
	matched := 0
	for _, c := range s {
		if matched < len(wanted) && c == wanted[matched] {
			matched++
		}
	}
	return int64(len(wanted) - matched)
}

var seed int64 = 2486

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := []rune{'a', 'b', 'c', 'd'}
	ss := make([][]rune, 20)
	ts := make([]string, 20)
	for g := 0; g < 20; g++ {
		ss[g] = make([]rune, 10000)
		for i := range ss[g] {
			ss[g][i] = letters[nextRandom()%4]
		}
		t := make([]rune, 10000)
		for i := range t {
			t[i] = letters[nextRandom()%4]
		}
		ts[g] = string(t)
	}
	check := int64(0)
	for p := int64(0); p < 600; p++ {
		for g := 0; g < 20; g++ {
			ss[g][check%10000] = letters[check/10000%4]
			s := string(ss[g])
			check = (check*31 + appendCharacters(s, ts[g]) + p) % 1000000007
		}
	}
	fmt.Printf("600 passes over 20 pairs of 10^4 letters: checksum %d\n", check)
}
