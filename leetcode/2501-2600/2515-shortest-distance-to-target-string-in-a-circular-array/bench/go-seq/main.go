// LeetCode #2515: Shortest Distance to Target String in a Circular Array
// -- Go mirror of the benchmark (closest.kara): the same lists, passes,
// order and checksum.
package main

import "fmt"

func closetTarget(words []string, target string, start int64) int64 {
	n := int64(len(words))
	best := int64(-1)
	for i := int64(0); i < n; i++ {
		if words[i] == target {
			d := i - start
			if d < 0 {
				d = -d
			}
			shortest := d
			if n-d < shortest {
				shortest = n - d
			}
			if best == -1 || shortest < best {
				best = shortest
			}
		}
	}
	return best
}

var seed int64 = 2515

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]string, 0, 2000)
	for l := 0; l < 2000; l++ {
		words := make([]string, 0, 100)
		for w := 0; w < 100; w++ {
			length := nextRandom()%3 + 1
			b := make([]byte, 0, length)
			for k := int64(0); k < length; k++ {
				b = append(b, byte('a'+nextRandom()%3))
			}
			words = append(words, string(b))
		}
		lists = append(lists, words)
	}
	const passes = 900
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, words := range lists {
			target := words[check/100%100]
			check = (check*31 + closetTarget(words, target, check%100) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 2000 lists of 100 words: checksum %d\n", passes, check)
}
