// LeetCode #2135: Count Words Obtained After Adding a Letter -- the
// benchmark, the same algorithm as words.kara.
package main

import "fmt"

func letters(w string) int64 {
	mask := int64(0)
	for i := 0; i < len(w); i++ {
		mask |= 1 << (w[i] - 97)
	}
	return mask
}

func wordCount(startWords, targetWords []string) int64 {
	starts := make(map[int64]struct{}, len(startWords))
	for _, w := range startWords {
		starts[letters(w)] = struct{}{}
	}
	count := int64(0)
	for _, w := range targetWords {
		mask := letters(w)
		for i := 0; i < len(w); i++ {
			if _, ok := starts[mask^(1<<(w[i]-97))]; ok {
				count++
				break
			}
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func word(length, k int64, seed *int64) string {
	letters := []byte("abcdefghijklmnopqrstuvwxyz"[:k])
	out := make([]byte, 0, length)
	for i := int64(0); i < length; i++ {
		j := i + nextRandom(seed)%(k-i)
		letters[i], letters[j] = letters[j], letters[i]
		out = append(out, letters[i])
	}
	return string(out)
}

func main() {
	seed := int64(2135)
	starts := make([][]string, 4)
	targets := make([][]string, 4)
	for p := 0; p < 4; p++ {
		for i := 0; i < 50000; i++ {
			length := nextRandom(&seed)%6 + 1
			starts[p] = append(starts[p], word(length, 12, &seed))
		}
		for i := 0; i < 50000; i++ {
			length := nextRandom(&seed)%6 + 1
			targets[p] = append(targets[p], word(length, 12, &seed))
		}
	}
	total, check := int64(0), int64(0)
	for round := int64(0); round < 25; round++ {
		for p := 0; p < 4; p++ {
			hi := nextRandom(&seed)
			a := (hi*32768 + nextRandom(&seed)) % 50000
			length := nextRandom(&seed)%6 + 1
			starts[p][a] = word(length, 12, &seed)
			hi = nextRandom(&seed)
			b := (hi*32768 + nextRandom(&seed)) % 50000
			length = nextRandom(&seed)%6 + 1
			targets[p][b] = word(length, 12, &seed)
			count := wordCount(starts[p], targets[p])
			total += count
			check = (check*31 + count + round) % 1000000007
		}
	}
	fmt.Printf("100 solves: %d words in all, checksum %d\n", total, check)
}
