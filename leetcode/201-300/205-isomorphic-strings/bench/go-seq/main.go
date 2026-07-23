package main

import "fmt"

func main() {
	var length, w, a int64 = 600000, 200, 20011
	s := make([]int64, length)
	t := make([]int64, length)
	var state int64 = 12345
	for i := int64(0); i < length; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		s[i] = state % a
	}
	for i := int64(0); i < length; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		t[i] = state % a
	}

	stVal := make([]int64, a)
	stVer := make([]int64, a)
	tsVal := make([]int64, a)
	tsVer := make([]int64, a)
	for z := int64(0); z < a; z++ {
		stVer[z] = -1
		tsVer[z] = -1
	}

	var sink int64 = 0
	last := length - w + 1
	for start := int64(0); start < last; start++ {
		stamp := start
		iso := true
		var k int64 = 0
		for iso && k < w {
			ch := s[start+k]
			dh := t[start+k]
			if stVer[ch] != stamp {
				stVer[ch] = stamp
				stVal[ch] = dh
			} else if stVal[ch] != dh {
				iso = false
			}
			if iso {
				if tsVer[dh] != stamp {
					tsVer[dh] = stamp
					tsVal[dh] = ch
				} else if tsVal[dh] != ch {
					iso = false
				}
			}
			k++
		}
		if iso {
			sink += 1
		}
	}
	fmt.Println(sink)
}
