// Benchmark mirror of parenrepair.kara — LeetCode #301, unique-by-construction
// repair. Same recursion, same depth-indexed scratch buffer, same sink.
package main

import "fmt"

const (
	ncases   = 2000
	slen     = 24
	passes   = 64
	slot     = 32
	maxdepth = 32
	mod      = int64(1000000007)
)

var (
	scratch  = make([]byte, maxdepth*slot)
	results  int64
	checksum int64
)

func repair(depth, length, lastI, lastJ int, open, close byte) {
	base := depth * slot
	child := base + slot

	count := 0
	for i := lastI; i < length; i++ {
		c := scratch[base+i]
		if c == open {
			count++
		} else if c == close {
			count--
		}
		if count < 0 {
			for j := lastJ; j <= i; j++ {
				if scratch[base+j] == close && (j == lastJ || scratch[base+j-1] != close) {
					w := 0
					for k := 0; k < length; k++ {
						if k != j {
							scratch[child+w] = scratch[base+k]
							w++
						}
					}
					repair(depth+1, length-1, i, j, open, close)
				}
			}
			return
		}
	}

	for r := 0; r < length; r++ {
		scratch[child+r] = scratch[base+length-1-r]
	}

	if open == '(' {
		repair(depth+1, length, 0, 0, ')', '(')
	} else {
		var h int64
		for t := 0; t < length; t++ {
			h = (h*31 + int64(scratch[child+t])) % mod
		}
		results++
		checksum = (checksum + h) % mod
	}
}

func main() {
	corpus := make([]byte, ncases*slen)
	state := int64(12345)
	for n := range corpus {
		state = (state*1103515245 + 12345) & 0x7fffffff
		r := (state / 65536) % 3
		switch r {
		case 0:
			corpus[n] = '('
		case 1:
			corpus[n] = ')'
		default:
			corpus[n] = 'a'
		}
	}

	for p := 0; p < passes; p++ {
		for ci := 0; ci < ncases; ci++ {
			copy(scratch[:slen], corpus[ci*slen:ci*slen+slen])
			repair(0, slen, 0, 0, '(', ')')
		}
	}

	fmt.Printf("results %d\n", results)
	fmt.Printf("checksum %d\n", checksum)
}
