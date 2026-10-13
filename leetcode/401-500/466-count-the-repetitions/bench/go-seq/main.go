// Benchmark for #466: mirror of count_repetitions.kara (the ★ arm: find
// the cycle) on the same workload. The memo of positions is a Go map,
// like the Kāra arm's Map.
package main

import "fmt"

func getMaxRepetitions(s1 string, n1 int64, s2 string, n2 int64) int64 {
	a := []byte(s1)
	b := []byte(s2)
	index := 0
	count := int64(0)
	seen := map[int][2]int64{}
	k := int64(0)
	for k < n1 {
		for _, c := range a {
			if c == b[index] {
				index++
				if index == len(b) {
					index = 0
					count++
				}
			}
		}
		k++
		if prev, ok := seen[index]; ok {
			cycle := k - prev[0]
			cycles := (n1 - k) / cycle
			count += cycles * (count - prev[1])
			k += cycles * cycle
			for k < n1 {
				for _, c := range a {
					if c == b[index] {
						index++
						if index == len(b) {
							index = 0
							count++
						}
					}
				}
				k++
			}
			break
		}
		seen[index] = [2]int64{k, count}
	}
	return count / n2
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const pairs = 100
	const rounds = 1000
	seed := int64(466)
	firsts := []string{}
	seconds := []string{}
	for p := 0; p < pairs; p++ {
		s1 := make([]byte, 100)
		for i := range s1 {
			s1[i] = byte(97 + nextRandom(&seed)%26)
		}
		n := 1 + nextRandom(&seed)%100
		s2 := make([]byte, n)
		for i := range s2 {
			s2[i] = s1[nextRandom(&seed)%100]
		}
		firsts = append(firsts, string(s1))
		seconds = append(seconds, string(s2))
	}
	total := int64(0)
	checksum := int64(0)
	for r := 0; r < rounds; r++ {
		for p := 0; p < pairs; p++ {
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			n1 := 1 + (hi*32768+lo)%1000000
			n2 := 1 + nextRandom(&seed)%100
			m := getMaxRepetitions(firsts[p], n1, seconds[p], n2)
			total += m
			checksum = (checksum*31 + m) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d pairs: %d repetitions in all, checksum %d\n", rounds, pairs, total, checksum)
}
