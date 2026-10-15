// LeetCode #686: Repeated String Match -- Knuth-Morris-Pratt. Bench.
//
// 100 pairs are built once: `a` of 1,000 to 10,000 letters over two
// letters, and `b` of 10,000 cut from the repetition of `a`, half of
// them with the last letter changed. Then 30 rounds answer every pair.
package main

import "fmt"

func repeatedStringMatch(a, b string) int64 {
	n := len(a)
	m := len(b)
	fail := make([]int, m)
	k := 0
	for i := 1; i < m; i++ {
		for k > 0 && b[i] != b[k] {
			k = fail[k-1]
		}
		if b[i] == b[k] {
			k++
		}
		fail[i] = k
	}
	j := 0
	for i := 0; i < n+m; i++ {
		c := a[i%n]
		for j > 0 && c != b[j] {
			j = fail[j-1]
		}
		if c == b[j] {
			j++
		}
		if j == m {
			return int64((i + 1 + n - 1) / n)
		}
	}
	return -1
}

var seed int64 = 686

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, m = 100, 30, 10000
	firsts := make([]string, 0, count)
	seconds := make([]string, 0, count)
	for c := 0; c < count; c++ {
		n := int(1000 + nextRandom()%9001)
		a := make([]byte, n)
		for i := range a {
			a[i] = byte(97 + nextRandom()%2)
		}
		start := int(nextRandom()) % n
		b := make([]byte, m)
		for i := range b {
			b[i] = a[(start+i)%n]
		}
		if c%2 == 1 {
			b[m-1] = 196 - b[m-1]
		}
		firsts = append(firsts, string(a))
		seconds = append(seconds, string(b))
	}
	var sum, none int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			k := repeatedStringMatch(firsts[c], seconds[c])
			if k == -1 {
				none++
			}
			sum = (sum*31 + k + r + 2) % 1000000007
		}
	}
	fmt.Printf("%d pairs answered: %d with no answer, checksum %d\n", count*rounds, none, sum)
}
