// LeetCode #65 — Go seq bench peer for valid.kara. Same algorithm,
// same workload, same sink as the Kara/Rust/C mirrors.

package main

import "fmt"

func categorize(b byte) int32 {
	if b >= '0' && b <= '9' {
		return 0
	}
	if b == '+' || b == '-' {
		return 1
	}
	if b == '.' {
		return 2
	}
	if b == 'e' || b == 'E' {
		return 3
	}
	return 4
}

func isNumber(s string) bool {
	bytes := []byte(s)
	n := len(bytes)

	state := int32(0)
	for i := 0; i < n; i++ {
		cat := categorize(bytes[i])

		switch state {
		case 0:
			switch cat {
			case 0:
				state = 2
			case 1:
				state = 1
			case 2:
				state = 3
			default:
				return false
			}
		case 1:
			switch cat {
			case 0:
				state = 2
			case 2:
				state = 3
			default:
				return false
			}
		case 2:
			switch cat {
			case 0:
				state = 2
			case 2:
				state = 4
			case 3:
				state = 6
			default:
				return false
			}
		case 3:
			switch cat {
			case 0:
				state = 5
			default:
				return false
			}
		case 4:
			switch cat {
			case 0:
				state = 5
			case 3:
				state = 6
			default:
				return false
			}
		case 5:
			switch cat {
			case 0:
				state = 5
			case 3:
				state = 6
			default:
				return false
			}
		case 6:
			switch cat {
			case 0:
				state = 8
			case 1:
				state = 7
			default:
				return false
			}
		case 7:
			switch cat {
			case 0:
				state = 8
			default:
				return false
			}
		case 8:
			switch cat {
			case 0:
				state = 8
			default:
				return false
			}
		default:
			return false
		}
	}

	return state == 2 || state == 4 || state == 5 || state == 8
}

func main() {
	const n int64 = 8
	const kIters int64 = 10000000

	inputs := []string{
		"0",
		"-.9",
		"53.5e93",
		"+6e-1",
		"abc",
		"1e",
		"99e2.5",
		"-123.456e789",
	}

	var sum int64
	for k := int64(0); k < kIters; k++ {
		idx := k % n
		if isNumber(inputs[idx]) {
			sum++
		}
	}
	fmt.Println(sum)
}
