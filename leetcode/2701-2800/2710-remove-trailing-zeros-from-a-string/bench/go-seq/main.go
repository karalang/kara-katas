// LeetCode #2710: Remove Trailing Zeros From a String -- the bench
// (zeros.kara in Go): an index walks back over the zeros, and the digits
// before it are copied out.
package main

import (
	"fmt"
	"strings"
)

func removeTrailingZeros(num string) string {
	end := len(num)
	for num[end-1] == '0' {
		end--
	}
	return strings.Clone(num[:end])
}

var seed int64 = 2710

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 20000, 20
	numbers := make([]string, 0, count)
	for c := 0; c < count; c++ {
		zeros := int(nextRandom() % 1000)
		b := make([]byte, 1000)
		b[0] = byte('1' + nextRandom()%9)
		for i := 1; i < 1000-zeros; i++ {
			b[i] = byte('0' + nextRandom()%10)
		}
		for i := 1000 - zeros; i < 1000; i++ {
			b[i] = '0'
		}
		numbers = append(numbers, string(b))
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, num := range numbers {
			out := removeTrailingZeros(num)
			kept := int64(len(out))
			sum += kept
			check = (check*31 + kept + int64(out[len(out)-1]) + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d numbers of 1000 digits, %d rounds: %d digits kept, checksum %d\n", count, rounds, sum, check)
}
