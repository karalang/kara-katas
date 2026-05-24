// LeetCode #8 — Go seq bench peer for atoi.kara. Same algorithm,
// same workload, same sink as the Kara/Rust/C mirrors.

package main

import "fmt"

func myAtoi(s string) int32 {
	bytes := []byte(s)
	n := len(bytes)

	const space byte = ' '
	const plus byte = '+'
	const minus byte = '-'
	const zero byte = '0'
	const nine byte = '9'

	i := 0
	for i < n && bytes[i] == space {
		i++
	}

	sign := int32(1)
	if i < n && bytes[i] == plus {
		i++
	} else if i < n && bytes[i] == minus {
		sign = -1
		i++
	}

	const intMax int32 = 2147483647
	const intMin int32 = -2147483648
	const maxDiv int32 = intMax / 10

	var result int32
	for i < n {
		b := bytes[i]
		if b < zero || b > nine {
			break
		}
		digit := int32(b - zero)
		if result > maxDiv || (result == maxDiv && digit > 7) {
			if sign == 1 {
				return intMax
			}
			return intMin
		}
		result = result*10 + digit
		i++
	}

	return sign * result
}

func main() {
	const n int64 = 8
	const kIters int64 = 10000000

	inputs := []string{
		"42",
		"   -42",
		"4193 with words",
		"91283472332",
		"+1",
		"  0000000000012345678",
		"-2147483648",
		"  -0012a42",
	}

	var sum int64
	for k := int64(0); k < kIters; k++ {
		idx := k % n
		sum += int64(myAtoi(inputs[idx]))
	}
	fmt.Println(sum)
}
