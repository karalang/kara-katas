// LeetCode #17 — Go seq bench peer for bench/letter_combinations.kara.
// Same M/K, generator, BFS shape, and sink as the Kara / Rust / C mirrors.

package main

import "fmt"

func letterCombinations(digits string) []string {
	if len(digits) == 0 {
		return nil
	}
	groups := [8]string{"abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"}
	out := []string{""}
	for _, d := range []byte(digits) {
		idx := int(d - '2')
		letters := groups[idx]
		prevLen := len(out)
		next := make([]string, 0, prevLen*len(letters))
		for i := 0; i < prevLen; i++ {
			prefix := out[i]
			for j := 0; j < len(letters); j++ {
				buf := make([]byte, 0, len(prefix)+1)
				buf = append(buf, prefix...)
				buf = append(buf, letters[j])
				next = append(next, string(buf))
			}
		}
		out = next
	}
	return out
}

func main() {
	const mCases int64 = 8
	const kIters int64 = 100_000
	cases := [8]string{"", "2", "7", "23", "79", "234", "279", "2349"}

	var sum int64 = 0
	for k := int64(0); k < kIters; k++ {
		idx := k % mCases
		r := letterCombinations(cases[idx])
		sum += int64(len(r))
	}
	fmt.Println(sum)
}
