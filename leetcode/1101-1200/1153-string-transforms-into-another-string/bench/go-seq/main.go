// LeetCode #1153 bench -- mirrors can_convert.kara: the same 64 pairs,
// the same rounds, the ★ arm's arrays.
package main

import "fmt"

func canConvert(str1, str2 string) bool {
	if str1 == str2 {
		return true
	}
	to := make([]int64, 26)
	used := make([]bool, 26)
	for i := range to {
		to[i] = -1
	}
	letters := 0
	for i := 0; i < len(str1); i++ {
		x := int(str1[i] - 'a')
		y := int64(str2[i] - 'a')
		if to[x] == -1 {
			to[x] = y
		} else if to[x] != y {
			return false
		}
		if !used[y] {
			used[y] = true
			letters++
		}
	}
	return letters < 26
}

var seed int64 = 1153

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 100000
	type pair struct{ a, b string }
	pairs := []pair{}
	for p := 0; p < 64; p++ {
		a := make([]byte, 10000)
		for i := range a {
			a[i] = byte('a' + nextRandom()%26)
		}
		mp := make([]byte, 26)
		for i := range mp {
			mp[i] = byte('a' + i)
		}
		for j := 25; j >= 1; j-- {
			k := nextRandom() % int64(j+1)
			mp[j], mp[k] = mp[k], mp[j]
		}
		if p%4 < 2 {
			mp[nextRandom()%26] = mp[25]
		}
		b := make([]byte, 10000)
		for i := range a {
			if p%4 == 3 {
				b[i] = a[i]
			} else {
				b[i] = mp[a[i]-'a']
			}
		}
		if p%4 == 1 {
			at := nextRandom() % 10000
			if b[at] == 'z' {
				b[at] = 'a'
			} else {
				b[at]++
			}
		}
		pairs = append(pairs, pair{string(a), string(b)})
	}
	yes := 0
	var check int64
	for r := 0; r < rounds; r++ {
		pr := pairs[r%64]
		ok := canConvert(pr.a, pr.b)
		v := int64(1)
		if ok {
			yes++
			v = 2
		}
		check = (check*31 + v + int64(r%64)) % 1000000007
	}
	fmt.Printf("%d rounds over 64 pairs of 10000 letters: %d convertible, checksum %d\n", rounds, yes, check)
}
