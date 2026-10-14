// Benchmark for #592: Go mirror of the ★ arm (a running sum, reduced as it
// goes); see ../fraction_addition.kara. The expression is turned into a
// []rune first, as the Kāra arm collects its characters.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func abs(a int64) int64 {
	if a < 0 {
		return -a
	}
	return a
}

func gcd(a, b int64) int64 {
	if b == 0 {
		return abs(a)
	}
	return gcd(b, a%b)
}

func digits(e []rune, i int) (int64, int) {
	var value int64
	j := i
	for j < len(e) && e[j] >= '0' && e[j] <= '9' {
		value = value*10 + int64(e[j]-'0')
		j++
	}
	return value, j
}

func fractionAddition(expression string) string {
	e := []rune(expression)
	var num, den int64 = 0, 1
	i := 0
	for i < len(e) {
		var sign int64 = 1
		if e[i] == '-' || e[i] == '+' {
			if e[i] == '-' {
				sign = -1
			}
			i++
		}
		a, afterA := digits(e, i)
		b, afterB := digits(e, afterA+1)
		i = afterB
		common := den / gcd(den, b) * b
		num = num*(common/den) + sign*a*(common/b)
		den = common
		g := gcd(num, den)
		num /= g
		den /= g
	}
	return strconv.FormatInt(num, 10) + "/" + strconv.FormatInt(den, 10)
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func coprime(a, b int64) bool {
	x, y := a, b
	for y != 0 {
		x, y = y, x%y
	}
	return x == 1
}

func expression(count int64, seed *int64) string {
	var out strings.Builder
	for k := int64(0); k < count; k++ {
		a := 1 + step(seed)%10
		b := 1 + step(seed)%10
		for !coprime(a, b) {
			a = 1 + step(seed)%10
			b = 1 + step(seed)%10
		}
		if step(seed)%2 == 0 {
			out.WriteByte('-')
		} else if k > 0 {
			out.WriteByte('+')
		}
		out.WriteString(strconv.FormatInt(a, 10) + "/" + strconv.FormatInt(b, 10))
	}
	return out.String()
}

func main() {
	count, rounds := 1000, 1000
	seed := int64(592)
	expressions := []string{}
	for k := 0; k < count; k++ {
		expressions = append(expressions, expression(10, &seed))
	}
	var negative, checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			got := fractionAddition(expressions[(round*7+g)%count])
			if strings.HasPrefix(got, "-") {
				negative++
			}
			for _, c := range got {
				checksum = (checksum*31 + int64(c)) % 1000000007
			}
		}
	}
	fmt.Printf("%d expressions, %d rounds: %d negative, checksum %d\n", count, rounds, negative, checksum)
}
