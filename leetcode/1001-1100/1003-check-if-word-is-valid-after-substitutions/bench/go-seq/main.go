// Benchmark: LeetCode #1003 Check If Word Is Valid After Substitutions --
// the ★ arm, a stack, on strings of 19998 letters, LeetCode's longest.
// Mirrors is_valid.kara, .c, .rs and .py.
package main

import "fmt"

func isValid(s string) bool {
	stack := []byte{}
	for i := 0; i < len(s); i++ {
		stack = append(stack, s[i])
		k := len(stack)
		if k >= 3 && stack[k-3] == 'a' && stack[k-2] == 'b' && stack[k-1] == 'c' {
			stack = stack[:k-3]
		}
	}
	return len(stack) == 0
}

var seed int64 = 1003

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// a valid string of `pieces` pieces, made left to right: each step
// either begins a new piece with its a or writes the next letter of the
// latest piece begun, at random
func randomValid(pieces int64) []byte {
	xs := []byte{}
	waiting := []byte{}
	left := pieces
	for left > 0 || len(waiting) > 0 {
		if left > 0 && (len(waiting) == 0 || nextRandom()%2 == 0) {
			xs = append(xs, 'a')
			waiting = append(waiting, 'b')
			left--
		} else {
			top := len(waiting) - 1
			c := waiting[top]
			xs = append(xs, c)
			if c == 'b' {
				waiting[top] = 'c'
			} else {
				waiting = waiting[:top]
			}
		}
	}
	return xs
}

func main() {
	rounds := 250
	// 20 strings of 6666 pieces, 19998 letters; the odd ones with one
	// letter changed
	letters := []byte{'a', 'b', 'c'}
	strings := []string{}
	for t := 0; t < 20; t++ {
		xs := randomValid(6666)
		if t%2 == 1 {
			at := nextRandom() % int64(len(xs))
			xs[at] = letters[(nextRandom()%2+1+int64(xs[at])-97)%3]
		}
		strings = append(strings, string(xs))
	}
	var valid, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			var v int64
			if isValid(strings[(r+i)%20]) {
				v = 1
			}
			valid += v
			check = (check*31 + v + int64(i) + 1) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 strings of 19998 letters: %d valid, checksum %d\n", rounds, valid, check)
}
