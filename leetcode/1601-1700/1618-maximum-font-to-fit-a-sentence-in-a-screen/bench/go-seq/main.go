// LeetCode #1618: Maximum Font to Fit a Sentence in a Screen -- the bench in
// Go, mirroring fonts.kara: a binary search for the last size that fits.
// The font is passed as its concrete type, as the Kāra generic is
// monomorphized.
package main

import "fmt"

type Font struct {
	base []int32
}

func (f *Font) GetWidth(fontSize int32, ch byte) int32 {
	return (fontSize*f.base[ch-'a'] + 3) / 4
}

func (f *Font) GetHeight(fontSize int32) int32 {
	return fontSize + fontSize/4
}

func fits(text string, w, h, size int32, info *Font) bool {
	if info.GetHeight(size) > h {
		return false
	}
	var sum int64
	for i := 0; i < len(text); i++ {
		sum += int64(info.GetWidth(size, text[i]))
	}
	return sum <= int64(w)
}

func maxFont(text string, w, h int32, fonts []int32, info *Font) int32 {
	lo, hi := 0, len(fonts)
	for lo < hi {
		mid := (lo + hi) / 2
		if fits(text, w, h, fonts[mid], info) {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	if lo == 0 {
		return -1
	}
	return fonts[lo-1]
}

var seed int64 = 1618

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	texts := make([]string, 200)
	for t := range texts {
		b := make([]byte, 5000)
		for i := range b {
			b[i] = byte('a' + nextRandom()%26)
		}
		texts[t] = string(b)
	}
	font := &Font{base: make([]int32, 26)}
	for k := range font.base {
		font.base[k] = int32(nextRandom()%8 + 1)
	}
	fonts := make([]int32, 60)
	for k := range fonts {
		fonts[k] = int32((k + 1) * 3)
	}
	var check, total int64
	for _, text := range texts {
		for q := 0; q < 40; q++ {
			w := int32(nextRandom()*8 + 1)
			h := int32(nextRandom()%240 + 1)
			answer := maxFont(text, w, h, fonts, font)
			check = (check*31 + int64(answer) + 1) % 1000000007
			total += int64(answer)
		}
	}
	fmt.Printf("8000 screens of 5000 letters: sizes total %d, checksum %d\n", total, check)
}
