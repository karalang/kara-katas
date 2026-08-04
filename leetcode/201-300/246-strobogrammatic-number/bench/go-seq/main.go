// Benchmark mirror for LeetCode #246 - Strobogrammatic Number.
//
// Same algorithm, same LCG, same sink as the Kara/C/Rust/Python mirrors.
// Byte-indexed (num[i] on a []byte), matching every other compiled lane: the
// input is ASCII digits, so all five index bytes in place and do the same work.
package main

import "fmt"

const (
	n      = 20000
	length = 32
	passes = 100
)

var (
	pairA = [5]byte{'0', '1', '8', '6', '9'}
	pairB = [5]byte{'0', '1', '8', '9', '6'}
	allD  = [10]byte{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
)

func rotateByte(b byte) byte {
	switch b {
	case '0':
		return '0'
	case '1':
		return '1'
	case '8':
		return '8'
	case '6':
		return '9'
	case '9':
		return '6'
	}
	return 0
}

func isStrobogrammatic(num []byte) bool {
	lo, hi := 0, len(num)-1
	for lo <= hi {
		r := rotateByte(num[lo])
		if r == 0 || r != num[hi] {
			return false
		}
		lo++
		hi--
	}
	return true
}

func lcg(state int64) int64 {
	return (state*1103515245 + 12345) & 2147483647
}

func main() {
	corpus := make([]byte, n*length)
	state := int64(1)
	for k := 0; k < n; k++ {
		num := corpus[k*length : (k+1)*length]
		lo, hi := 0, length-1
		for lo < hi {
			state = lcg(state)
			p := (state / 65536) % 5
			num[lo] = pairA[p]
			num[hi] = pairB[p]
			lo++
			hi--
		}
		state = lcg(state)
		if (state/65536)%8 == 0 {
			state = lcg(state)
			pos := (state / 65536) % length
			state = lcg(state)
			num[pos] = allD[(state/65536)%10]
		}
	}

	var acc int64
	for p := 0; p < passes; p++ {
		for i := 0; i < n; i++ {
			v := int64(0)
			if isStrobogrammatic(corpus[i*length : (i+1)*length]) {
				v = 1
			}
			acc = (acc*131 + v) % 1000000007
		}
	}
	fmt.Println(acc)
}
