// LeetCode #2433: Find The Original Array of Prefix Xor -- the bench, the
// ★ arm: every value its prefix XOR the prefix before, the first its own
// prefix, gathered into a new list.
package main

import "fmt"

func findArray(pref []int64) []int64 {
	var arr []int64
	var before int64
	for _, p := range pref {
		arr = append(arr, p^before)
		before = p
	}
	return arr
}

var seed int64 = 2433

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var pref []int64
	for i := 0; i < 100000; i++ {
		a := nextRandom()
		pref = append(pref, (a*32768+nextRandom())%1000001)
	}
	var check int64
	for p := int64(0); p < 1000; p++ {
		pref[(p*7919)%100000] = p
		arr := findArray(pref)
		for _, v := range arr {
			check = (check*31 + v) % 1000000007
		}
	}
	fmt.Printf("1000 passes over 10^5 prefixes: checksum %d\n", check)
}
