// LeetCode #1487: Making File Names Unique -- bench, the Go twin of
// get_folder_names.kara.
package main

import "fmt"

func getFolderNames(names []string) []string {
	next := map[string]int64{}
	out := make([]string, 0, len(names))
	for _, name := range names {
		from, ok := next[name]
		if !ok {
			next[name] = 1
			out = append(out, name)
			continue
		}
		k := from
		for {
			if _, taken := next[fmt.Sprintf("%s(%d)", name, k)]; !taken {
				break
			}
			k++
		}
		made := fmt.Sprintf("%s(%d)", name, k)
		next[name] = k + 1
		next[made] = 1
		out = append(out, made)
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func nameOf(b int64, suffix int64) string {
	base := fmt.Sprintf("%c%d", rune('a'+b%26), b/26)
	if suffix == 0 {
		return base
	}
	return fmt.Sprintf("%s(%d)", base, suffix)
}

func main() {
	seed := int64(1487)
	names := make([]string, 0, 50000)
	for i := 0; i < 50000; i++ {
		b := nextRandom(&seed) % 3000
		s := nextRandom(&seed) % 9
		if s < 3 {
			names = append(names, nameOf(b, s+1))
		} else {
			names = append(names, nameOf(b, 0))
		}
	}
	var check int64
	for pass := int64(0); pass < 20; pass++ {
		names[check%50000] = nameOf(check%3000, check%4)
		folders := getFolderNames(names)
		for _, f := range folders {
			for i := 0; i < len(f); i++ {
				check = (check*131 + int64(f[i])) % 1000000007
			}
		}
		check = (check + pass) % 1000000007
	}
	fmt.Printf("20 passes over 50000 names: checksum %d\n", check)
}
