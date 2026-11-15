// LeetCode #2129: Capitalize the Title -- the benchmark, the same
// algorithm as title.kara.
package main

import (
	"fmt"
	"strings"
)

func capitalizeTitle(title string) string {
	words := strings.Split(title, " ")
	for i, w := range words {
		lower := strings.ToLower(w)
		if len(lower) <= 2 {
			words[i] = lower
		} else {
			words[i] = strings.ToUpper(lower[:1]) + lower[1:]
		}
	}
	return strings.Join(words, " ")
}

var seed int64 = 2129

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	titles := make([][]byte, 1000)
	for k := range titles {
		t := []byte{}
		for {
			n := int(nextRandom()%6 + 1)
			if len(t)+1+n > 100 {
				break
			}
			if len(t) > 0 {
				t = append(t, ' ')
			}
			for i := 0; i < n; i++ {
				c := nextRandom() % 52
				if c < 26 {
					t = append(t, byte(97+c))
				} else {
					t = append(t, byte(39+c))
				}
			}
		}
		titles[k] = t
	}
	var capitals, check int64
	for round := int64(0); round < 200; round++ {
		for k := 0; k < 1000; k++ {
			n := int64(len(titles[k]))
			p := nextRandom() % n
			if titles[k][p] == ' ' {
				p--
			}
			titles[k][p] ^= 32
			title := string(titles[k])
			answer := capitalizeTitle(title)
			for i := 0; i < len(answer); i++ {
				b := int64(answer[i])
				if b >= 65 && b <= 90 {
					capitals++
				}
				check = (check*31 + b + round) % 1000000007
			}
		}
	}
	fmt.Printf("200000 titles: %d capitals, checksum %d\n", capitals, check)
}
