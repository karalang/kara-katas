// Benchmark for #854: K-Similar Strings -- Go twin of the Kāra ★ arm
// (breadth-first search over swaps that fix a letter).
package main

import "fmt"

func kSimilarity(s1, s2 string) int64 {
	goal := []byte(s2)
	n := len(goal)
	seen := map[string]struct{}{s1: {}}
	level := [][]byte{[]byte(s1)}
	var swaps int64
	for {
		var next [][]byte
		for _, cur := range level {
			i := 0
			for i < n && cur[i] == goal[i] {
				i++
			}
			if i == n {
				return swaps
			}
			for j := i + 1; j < n; j++ {
				if cur[j] == goal[i] && cur[j] != goal[j] {
					moved := append([]byte(nil), cur...)
					moved[i], moved[j] = moved[j], moved[i]
					key := string(moved)
					if _, ok := seen[key]; !ok {
						seen[key] = struct{}{}
						next = append(next, moved)
					}
				}
			}
		}
		level = next
		swaps++
	}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 64, 6400, 20
	var seed int64 = 854
	firsts := make([]string, 0, count)
	seconds := make([]string, 0, count)
	for g := int64(0); g < count; g++ {
		letters := 2 + g%5
		a := make([]byte, 0, n)
		for i := 0; i < n; i++ {
			a = append(a, byte('a'+nextRandom(&seed)%letters))
		}
		b := append([]byte(nil), a...)
		for i := n - 1; i >= 1; i-- {
			j := nextRandom(&seed) % int64(i+1)
			b[i], b[j] = b[j], b[i]
		}
		firsts = append(firsts, string(a))
		seconds = append(seconds, string(b))
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		g := round % count
		k := kSimilarity(firsts[g], seconds[g])
		total += k
		checksum = (checksum*31 + k) % 1000000007
	}
	fmt.Printf("%d rounds of %d pairs: swaps sum to %d, checksum %d\n", rounds, count, total, checksum)
}
