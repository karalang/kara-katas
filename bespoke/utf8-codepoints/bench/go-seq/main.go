// Go mirror of the utf8-codepoints decode bench — same algorithm, same sink.
package main

import "fmt"

const (
	MODULUS = 1000000007
	REPEAT  = 9523
	ITERS   = 400
)

func utf8ByteLen(lead byte) int {
	switch {
	case lead < 0x80:
		return 1
	case lead >= 0xC0 && lead <= 0xDF:
		return 2
	case lead >= 0xE0 && lead <= 0xEF:
		return 3
	case lead >= 0xF0 && lead <= 0xF7:
		return 4
	default:
		return 1
	}
}

func main() {
	cps := []rune{
		0x61, 0x62, 0x63, 0x20, 0x31, 0x32, 0x33, 0x20,
		0xe9, 0xf1, 0x3b1, 0x3b2, 0x434, 0x436,
		0x65e5, 0x672c, 0x1d11e, 0x1f980, 0x20,
	}
	base := string(cps)
	var sb []byte
	for r := 0; r < REPEAT; r++ {
		sb = append(sb, base...)
	}
	buf := sb
	n := len(buf)

	var sink int64 = 0
	var count int64 = 0
	for t := 0; t < ITERS; t++ {
		i := 0
		for i < n {
			lead := buf[i]
			ln := utf8ByteLen(lead)
			var cp int64
			switch ln {
			case 1:
				cp = int64(lead)
			case 2:
				cp = int64(lead & 0x1F)
			case 3:
				cp = int64(lead & 0x0F)
			default:
				cp = int64(lead & 0x07)
			}
			k := 1
			for k < ln && i+k < n {
				cp = (cp << 6) | int64(buf[i+k]&0x3F)
				k++
			}
			sink = (sink + cp) % MODULUS
			count++
			i += ln
		}
	}
	fmt.Printf("%d %d\n", count, sink)
}
