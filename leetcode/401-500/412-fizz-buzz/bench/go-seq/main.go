// Benchmark for #412: mirror of fizz_buzz.kara (test each case). Go's
// string literals are not copied, so only the numbers allocate.
package main

import (
	"fmt"
	"os"
	"strconv"
)

func fizzBuzz(n int64) []string {
	answer := []string{}
	for i := int64(1); i <= n; i++ {
		if i%15 == 0 {
			answer = append(answer, "FizzBuzz")
		} else if i%3 == 0 {
			answer = append(answer, "Fizz")
		} else if i%5 == 0 {
			answer = append(answer, "Buzz")
		} else {
			answer = append(answer, strconv.FormatInt(i, 10))
		}
	}
	return answer
}

var seed int64 = 412

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var calls int64 = 2000
	if len(os.Args) > 1 {
		calls, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	var bytes, checksum int64
	for c := int64(0); c < calls; c++ {
		n := 9000 + step()%1001
		answer := fizzBuzz(n)
		var length int64
		for _, s := range answer {
			length += int64(len(s))
		}
		bytes += length
		checksum = (checksum*31 + length) % 1000000007
	}
	fmt.Printf("%d calls: %d bytes, checksum %d\n", calls, bytes, checksum)
}
