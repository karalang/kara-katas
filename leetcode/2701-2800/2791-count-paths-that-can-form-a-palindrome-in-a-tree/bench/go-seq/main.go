// LeetCode #2791: Count Paths That Can Form a Palindrome in a Tree -- the
// bench in Go: the ★ arm over 20 random trees of 10^5 nodes with letters
// from a to z, all drawn first, then each answered 5 times.
package main

import "fmt"

func countPalindromePaths(parent []int64, s string) int64 {
	n := len(parent)
	children := make([][]int, n)
	for i := 1; i < n; i++ {
		children[parent[i]] = append(children[parent[i]], i)
	}
	mask := make([]int64, n)
	todo := []int{0}
	for len(todo) > 0 {
		u := todo[len(todo)-1]
		todo = todo[:len(todo)-1]
		for _, c := range children[u] {
			mask[c] = mask[u] ^ (1 << (s[c] - 'a'))
			todo = append(todo, c)
		}
	}
	seen := map[int64]int64{}
	var paths int64
	for _, m := range mask {
		paths += seen[m]
		for b := 0; b < 26; b++ {
			paths += seen[m^(1<<b)]
		}
		seen[m]++
	}
	return paths
}

var seed int64 = 2791

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count := 20
	rounds := 5
	n := 100000
	parents := make([][]int64, count)
	letters := make([]string, count)
	for c := 0; c < count; c++ {
		parents[c] = make([]int64, n)
		parents[c][0] = -1
		for i := 1; i < n; i++ {
			parents[c][i] = wide() % int64(i)
		}
		b := make([]byte, n)
		for i := range b {
			b[i] = byte('a' + nextRandom()%26)
		}
		letters[c] = string(b)
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := countPalindromePaths(parents[c], letters[c])
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d trees of 10^5, %d rounds: paths sum to %d, checksum %d\n", count, rounds, total, check)
}
