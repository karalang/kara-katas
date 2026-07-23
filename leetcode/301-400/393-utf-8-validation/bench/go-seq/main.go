package main

import "fmt"

func leadLen(b byte) int64 {
	if b&0x80 == 0x00 {
		return 1
	} else if b&0xE0 == 0xC0 {
		return 2
	} else if b&0xF0 == 0xE0 {
		return 3
	} else if b&0xF8 == 0xF0 {
		return 4
	}
	return 0
}

func isContinuation(b byte) bool {
	return b&0xC0 == 0x80
}

func validateWindow(data []byte, base, w int64) bool {
	end := base + w
	i := base
	for i < end {
		need := leadLen(data[i])
		if need == 0 {
			return false
		}
		if i+need > end {
			return false
		}
		for k := int64(1); k < need; k++ {
			if !isContinuation(data[i+k]) {
				return false
			}
		}
		i += need
	}
	return true
}

func main() {
	var records, w, passes int64 = 40000, 32, 60
	total := records * w

	data := make([]byte, total)

	var state int64 = 12345
	for rec := int64(0); rec < records; rec++ {
		base := rec * w
		filled := int64(0)
		for filled < w {
			state = (state*1103515245 + 12345) & 2147483647
			r := state >> 16
			cat := r % 100
			sub := r / 100
			rem := w - filled
			if cat < 8 {
				data[base+filled] = byte(128 + (sub % 64))
				filled += 1
			} else if cat < 60 || rem < 2 {
				data[base+filled] = byte(sub % 128)
				filled += 1
			} else if cat < 80 || rem < 3 {
				data[base+filled] = byte(192 + (sub % 32))
				data[base+filled+1] = byte(128 + (sub % 64))
				filled += 2
			} else if cat < 93 || rem < 4 {
				data[base+filled] = byte(224 + (sub % 16))
				data[base+filled+1] = byte(128 + (sub % 64))
				data[base+filled+2] = byte(128 + (sub % 64))
				filled += 3
			} else {
				data[base+filled] = byte(240 + (sub % 8))
				data[base+filled+1] = byte(128 + (sub % 64))
				data[base+filled+2] = byte(128 + (sub % 64))
				data[base+filled+3] = byte(128 + (sub % 64))
				filled += 4
			}
		}
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := (p * 40009) % total
		data[idx] = byte(255 - int64(data[idx]))

		var count int64 = 0
		for rec := int64(0); rec < records; rec++ {
			if validateWindow(data, rec*w, w) {
				count++
			}
		}
		sink += count
	}
	fmt.Println(sink)
}
