// Benchmark for #843: Guess the Word -- Go twin of the Kāra ★ arm (minimax
// over the words still possible).
package main

import "fmt"

type Master struct {
	words   []string
	secret  string
	guesses int64
	found   bool
}

func (m *Master) guess(word string) int64 {
	m.guesses++
	listed := false
	for _, w := range m.words {
		if w == word {
			listed = true
			break
		}
	}
	if !listed {
		return -1
	}
	if word == m.secret && m.guesses <= 10 {
		m.found = true
	}
	var count int64
	for k := 0; k < 6; k++ {
		if word[k] == m.secret[k] {
			count++
		}
	}
	return count
}

func shared(a, b []byte) int64 {
	var count int64
	for k := range a {
		if a[k] == b[k] {
			count++
		}
	}
	return count
}

func findSecretWord(words []string, master *Master) {
	n := len(words)
	letters := make([][]byte, n)
	for i, w := range words {
		letters[i] = []byte(w)
	}
	same := make([][]int64, n)
	for i := 0; i < n; i++ {
		same[i] = make([]int64, n)
		for j := 0; j < n; j++ {
			same[i][j] = shared(letters[i], letters[j])
		}
	}
	possible := make([]int, n)
	for i := range possible {
		possible[i] = i
	}
	for len(possible) > 0 {
		best := possible[0]
		bestWorst := int64(n + 1)
		for _, c := range possible {
			var groups [7]int64
			for _, o := range possible {
				groups[same[c][o]]++
			}
			var worst int64
			for k := 0; k < 6; k++ {
				if groups[k] > worst {
					worst = groups[k]
				}
			}
			if worst < bestWorst {
				bestWorst = worst
				best = c
			}
		}
		answer := master.guess(words[best])
		if answer == 6 {
			return
		}
		left := []int{}
		for _, o := range possible {
			if same[best][o] == answer {
				left = append(left, o)
			}
		}
		possible = left
	}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func contains(words []string, w string) bool {
	for _, x := range words {
		if x == w {
			return true
		}
	}
	return false
}

func main() {
	const count, rounds = 64, 6000
	seed := int64(843)
	lists := make([][]string, 0, count)
	masters := make([]*Master, 0, count)
	ks := []int64{4, 8, 16, 26}
	for g := 0; g < count; g++ {
		k := ks[g%4]
		words := []string{}
		for len(words) < 100 {
			b := make([]byte, 6)
			for i := range b {
				b[i] = byte(97 + nextRandom(&seed)%k)
			}
			w := string(b)
			if !contains(words, w) {
				words = append(words, w)
			}
		}
		secret := words[nextRandom(&seed)%100]
		masters = append(masters, &Master{words: append([]string{}, words...), secret: secret})
		lists = append(lists, words)
	}
	found, checksum := 0, int64(0)
	for round := 0; round < rounds; round++ {
		g := round % count
		masters[g].guesses = 0
		masters[g].found = false
		findSecretWord(lists[g], masters[g])
		if masters[g].found {
			found++
		}
		checksum = (checksum*31 + masters[g].guesses) % 1000000007
	}
	fmt.Printf("%d rounds of %d lists: %d found, checksum %d\n", rounds, count, found, checksum)
}
