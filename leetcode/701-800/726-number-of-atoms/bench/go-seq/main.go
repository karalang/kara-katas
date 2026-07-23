package main

import "fmt"

func isUpper(b byte) bool { return b >= 'A' && b <= 'Z' }
func isLower(b byte) bool { return b >= 'a' && b <= 'z' }
func isDigit(b byte) bool { return b >= '0' && b <= '9' }

func drawHi(state *int64) int64 {
	*state = (*state*1103515245 + 12345) & 2147483647
	return *state >> 16
}

func emitElement(buf *[]byte, dpos *[]int64, state *int64) {
	du := drawHi(state)
	*buf = append(*buf, byte('A'+du%6))
	if (du/6)%2 == 0 {
		dl := drawHi(state)
		*buf = append(*buf, byte('a'+dl%3))
	}
	dc := drawHi(state)
	*buf = append(*buf, byte('1'+dc%9))
	*dpos = append(*dpos, int64(len(*buf))-1)
}

func emitMult(buf *[]byte, dpos *[]int64, state *int64) {
	dm := drawHi(state)
	*buf = append(*buf, byte('0'+2+dm%8))
	*dpos = append(*dpos, int64(len(*buf))-1)
}

func main() {
	var numChunks, passes, idRange int64 = 20000, 400, 24

	buf := make([]byte, 0)
	dpos := make([]int64, 0)
	var state int64 = 12345

	for ch := int64(0); ch < numChunks; ch++ {
		tt := drawHi(&state) % 5
		if tt == 0 {
			emitElement(&buf, &dpos, &state)
		} else if tt == 1 {
			emitElement(&buf, &dpos, &state)
			emitElement(&buf, &dpos, &state)
		} else if tt == 2 {
			buf = append(buf, '(')
			emitElement(&buf, &dpos, &state)
			emitElement(&buf, &dpos, &state)
			buf = append(buf, ')')
			emitMult(&buf, &dpos, &state)
		} else if tt == 3 {
			buf = append(buf, '(')
			emitElement(&buf, &dpos, &state)
			buf = append(buf, '(')
			emitElement(&buf, &dpos, &state)
			emitElement(&buf, &dpos, &state)
			buf = append(buf, ')')
			emitMult(&buf, &dpos, &state)
			buf = append(buf, ')')
			emitMult(&buf, &dpos, &state)
		} else {
			buf = append(buf, '(')
			emitElement(&buf, &dpos, &state)
			emitElement(&buf, &dpos, &state)
			emitElement(&buf, &dpos, &state)
			buf = append(buf, ')')
			emitMult(&buf, &dpos, &state)
		}
	}

	n := int64(len(buf))
	ndig := int64(len(dpos))

	nid := make([]int64, 0)
	counts := make([]int64, 0)
	pst := make([]int64, 0)
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		pos := dpos[p%ndig]
		buf[pos] = byte('1' + ((int64(buf[pos]) - '1' + 1) % 9))

		nid = nid[:0]
		counts = counts[:0]
		pst = pst[:0]

		i := int64(0)
		for i < n {
			b := buf[i]
			if b == '(' {
				pst = append(pst, int64(len(nid)))
				i++
			} else if b == ')' {
				i++
				var mult int64 = 0
				have := false
				for i < n && isDigit(buf[i]) {
					mult = mult*10 + int64(buf[i]-'0')
					have = true
					i++
				}
				if !have {
					mult = 1
				}
				start := pst[len(pst)-1]
				pst = pst[:len(pst)-1]
				for k := start; k < int64(len(nid)); k++ {
					counts[k] *= mult
				}
			} else if isUpper(b) {
				up := int64(b - 'A')
				i++
				var low int64 = 0
				if i < n && isLower(buf[i]) {
					low = int64(buf[i]-'a') + 1
					i++
				}
				id := up*4 + low
				var c int64 = 0
				have := false
				for i < n && isDigit(buf[i]) {
					c = c*10 + int64(buf[i]-'0')
					have = true
					i++
				}
				if !have {
					c = 1
				}
				nid = append(nid, id)
				counts = append(counts, c)
			} else {
				i++
			}
		}

		m := make(map[int64]int64)
		for e := 0; e < len(nid); e++ {
			m[nid[e]] += counts[e]
		}

		var checksum int64 = 0
		for id2 := int64(0); id2 < idRange; id2++ {
			checksum += id2 * m[id2]
		}
		sink += checksum
	}
	fmt.Println(sink)
}
