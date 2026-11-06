// LeetCode #1055: Shortest Way to Form String -- Go mirror of
// bench/shortest_way.kara.
package main

import "fmt"

var seed int64 = 1055

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func shortestWay(s, t []byte) int64 {
	var pieces int64
	i := 0
	for i < len(t) {
		start := i
		for _, c := range s {
			if i < len(t) && t[i] == c {
				i++
			}
		}
		if i == start {
			return -1
		}
		pieces++
	}
	return pieces
}

func randomWord(n int) []byte {
	w := make([]byte, n)
	for k := range w {
		w[k] = byte(97 + nextRandom()%20)
	}
	return w
}

func main() {
	const count, rounds = 100, 10
	sources := make([][]byte, count)
	targets := make([][]byte, count)
	for a := 0; a < count; a++ {
		sources[a] = randomWord(1000)
		targets[a] = randomWord(10000)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for a := 0; a < count; a++ {
			answer := shortestWay(sources[a], targets[a])
			total += answer
			check = (check*131 + answer) % 1000000007
		}
	}
	fmt.Printf("%d pairs of 1000 and 10000 letters, %d rounds: total %d, checksum %d\n", count, rounds, total, check)
}
