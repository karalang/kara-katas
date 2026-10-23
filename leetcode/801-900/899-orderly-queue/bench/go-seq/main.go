// LeetCode #899 bench: the counts arm (rotations compared in place,
// letters counted) on 1,000 strings of 1,000 letters, LeetCode's largest,
// each a random piece of 1 to 4 letters written over and over with one
// letter changed at a random place, so that rotations agree for long
// stretches before they differ. Every string is asked with k = 1, and
// with k = 2 as well. The same algorithm as orderly_queue.kara.
package main

import "fmt"

func orderlyQueue(b []byte, k int64) []byte {
	n := int64(len(b))
	out := make([]byte, 0, n)
	if k == 1 {
		best := int64(0)
		for i := int64(1); i < n; i++ {
			d := int64(0)
			for d < n && b[(i+d)%n] == b[(best+d)%n] {
				d++
			}
			if d < n && b[(i+d)%n] < b[(best+d)%n] {
				best = i
			}
		}
		for j := int64(0); j < n; j++ {
			out = append(out, b[(best+j)%n])
		}
		return out
	}
	var count [26]int64
	for _, c := range b {
		count[c-97]++
	}
	for letter := 0; letter < 26; letter++ {
		for c := int64(0); c < count[letter]; c++ {
			out = append(out, byte(97+letter))
		}
	}
	return out
}

var seed int64 = 899

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func checksum(s []byte, check int64) int64 {
	for _, b := range s {
		check = (check*131 + int64(b)) % 1000000007
	}
	return check
}

func main() {
	var check int64
	for r := 0; r < 1000; r++ {
		p := 1 + nextRandom()%4
		piece := make([]byte, 0, p)
		for i := int64(0); i < p; i++ {
			piece = append(piece, byte(97+nextRandom()%26))
		}
		changed := nextRandom() % 1000
		letter := byte(97 + nextRandom()%26)
		s := make([]byte, 1000)
		for i := int64(0); i < 1000; i++ {
			if i == changed {
				s[i] = letter
			} else {
				s[i] = piece[i%p]
			}
		}
		check = checksum(orderlyQueue(s, 1), check)
		check = checksum(orderlyQueue(s, 2), check)
	}
	fmt.Printf("1000 strings of 1000 letters, k = 1 and 2: checksum %d\n", check)
}
