// LeetCode #2166: Design Bitset -- the benchmark's Go mirror of
// bitset.kara.
package main

import (
	"fmt"
	"strings"
)

type Bitset struct {
	bits    []bool
	flipped bool
	ones    int64
}

func newBitset(size int64) *Bitset {
	return &Bitset{bits: make([]bool, size)}
}

func (b *Bitset) fix(idx int64) {
	if b.bits[idx] == b.flipped {
		b.bits[idx] = !b.flipped
		b.ones++
	}
}

func (b *Bitset) unfix(idx int64) {
	if b.bits[idx] != b.flipped {
		b.bits[idx] = b.flipped
		b.ones--
	}
}

func (b *Bitset) flip() {
	b.flipped = !b.flipped
	b.ones = int64(len(b.bits)) - b.ones
}

func (b *Bitset) all() bool   { return b.ones == int64(len(b.bits)) }
func (b *Bitset) one() bool   { return b.ones > 0 }
func (b *Bitset) count() int64 { return b.ones }

func (b *Bitset) toString() string {
	var text strings.Builder
	for _, bit := range b.bits {
		if bit != b.flipped {
			text.WriteByte('1')
		} else {
			text.WriteByte('0')
		}
	}
	return text.String()
}

var seed int64 = 2166

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var size int64 = 100000
	bits := newBitset(size)
	var check int64
	for i := 0; i < 5000000; i++ {
		if i%500000 == 499999 {
			text := bits.toString()
			for k := 0; k < len(text); k++ {
				check = (check*31 + int64(text[k])) % 1000000007
			}
			continue
		}
		pick := nextRandom() % 16
		var answer int64
		if pick < 7 {
			hi := nextRandom()
			bits.fix((hi*32768 + nextRandom()) % size)
		} else if pick < 13 {
			hi := nextRandom()
			bits.unfix((hi*32768 + nextRandom()) % size)
		} else if pick == 13 {
			bits.flip()
		} else if pick == 14 {
			if bits.all() {
				answer = 2
			} else if bits.one() {
				answer = 1
			}
		} else {
			answer = bits.count()
		}
		check = (check*31 + answer) % 1000000007
	}
	fmt.Printf("5000000 calls: checksum %d\n", check)
}
