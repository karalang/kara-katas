// Benchmark for #423: mirror of original_digits.kara (unique letters).
package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func originalDigits(s string) string {
	var letters [26]int64
	for i := 0; i < len(s); i++ {
		letters[s[i]-'a']++
	}
	at := func(c byte) int64 { return letters[c-'a'] }
	var count [10]int64
	count[0] = at('z')
	count[2] = at('w')
	count[4] = at('u')
	count[6] = at('x')
	count[8] = at('g')
	count[3] = at('h') - count[8]
	count[5] = at('f') - count[4]
	count[7] = at('s') - count[6]
	count[1] = at('o') - count[0] - count[2] - count[4]
	count[9] = at('i') - count[5] - count[6] - count[8]
	var out strings.Builder
	for d := 0; d < 10; d++ {
		for t := int64(0); t < count[d]; t++ {
			out.WriteByte(byte('0' + d))
		}
	}
	return out.String()
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	calls := int64(100000)
	if len(os.Args) > 1 {
		calls, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	blocks := int64(20000)
	names := []string{"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}
	seed := int64(423)
	text := make([]byte, 0)
	ends := []int{0}
	for b := int64(0); b < blocks; b++ {
		count := 1 + step(&seed)%8
		pool := make([]byte, 0)
		for c := int64(0); c < count; c++ {
			pool = append(pool, names[step(&seed)%10]...)
		}
		for i := 0; i < len(pool); i++ {
			j := i + int(step(&seed)%int64(len(pool)-i))
			pool[i], pool[j] = pool[j], pool[i]
		}
		text = append(text, pool...)
		ends = append(ends, len(text))
	}
	s := string(text)
	var digits, checksum int64
	for c := int64(0); c < calls; c++ {
		length := 50 + step(&seed)%200
		first := step(&seed) % (blocks - length)
		answer := originalDigits(s[ends[first]:ends[first+length]])
		digits += int64(len(answer))
		for k := 0; k < len(answer); k++ {
			checksum = (checksum*31 + int64(answer[k]) - 47) % 1000000007
		}
	}
	fmt.Printf("%d calls on %d letters: %d digits, checksum %d\n", calls, len(s), digits, checksum)
}
