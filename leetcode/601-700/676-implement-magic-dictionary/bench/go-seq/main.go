// Benchmark for #676: every word of the same length compared, as the
// Kara ★ arm.
package main

import "fmt"

type MagicDictionary struct {
	words []string
}

func (d *MagicDictionary) buildDict(dictionary []string) {
	d.words = append([]string(nil), dictionary...)
}

func (d *MagicDictionary) search(searchWord string) bool {
	b := []byte(searchWord)
	for _, w := range d.words {
		a := []byte(w)
		if len(a) == len(b) {
			diff := 0
			for i := range a {
				if a[i] != b[i] {
					diff++
				}
			}
			if diff == 1 {
				return true
			}
		}
	}
	return false
}

var seed int64 = 676

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(length int) string {
	s := make([]byte, 0, length)
	for i := 0; i < length; i++ {
		s = append(s, byte(97+nextRandom()%2))
	}
	return string(s)
}

func main() {
	rounds := 1000
	var sum int64
	found := 0
	for r := 0; r < rounds; r++ {
		dictionary := make([]string, 0)
		for i := 0; i < 100; i++ {
			dictionary = append(dictionary, randomWord(50))
		}
		d := &MagicDictionary{}
		d.buildDict(dictionary)
		for k := 0; k < 100; k++ {
			var word string
			if k%2 == 0 {
				w := dictionary[nextRandom()%100]
				at := nextRandom() % 50
				c := "a"
				if w[at:at+1] == "a" {
					c = "b"
				}
				word = w[:at] + c + w[at+1:]
			} else {
				word = randomWord(50)
			}
			if d.search(word) {
				found++
				sum = (sum*3 + 1) % 1000000007
			} else {
				sum = sum * 3 % 1000000007
			}
		}
	}
	fmt.Printf("%d dictionaries of 100 words, %d searches, %d found: checksum %d\n", rounds, rounds*100, found, sum)
}
