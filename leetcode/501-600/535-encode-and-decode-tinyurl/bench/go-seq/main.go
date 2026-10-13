// Benchmark for #535: the ★ arm (a counter written in base 62); see
// ../../README.md § Benchmarks. Mirrors encode_and_decode_tinyurl.kara.
package main

import "fmt"

const prefix = "http://tinyurl.com/"

func digit(d int64) byte {
	if d < 10 {
		return byte('0' + d)
	} else if d < 36 {
		return byte('a' + d - 10)
	}
	return byte('A' + d - 36)
}

func base62(n int64) string {
	rev := []byte{}
	m := n
	for {
		rev = append(rev, digit(m%62))
		m /= 62
		if m == 0 {
			break
		}
	}
	code := make([]byte, 0, len(rev))
	for i := len(rev) - 1; i >= 0; i-- {
		code = append(code, rev[i])
	}
	return string(code)
}

type Codec struct {
	byCode map[string]string
	byURL  map[string]string
	next   int64
}

func newCodec() *Codec {
	return &Codec{byCode: map[string]string{}, byURL: map[string]string{}}
}

func (c *Codec) encode(longURL string) string {
	code, ok := c.byURL[longURL]
	if !ok {
		code = base62(c.next)
		c.next++
		c.byCode[code] = longURL
		c.byURL[longURL] = code
	}
	return prefix + code
}

func (c *Codec) decode(shortURL string) string {
	return c.byCode[shortURL[len(prefix):]]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomURL(seed *int64, most int64) string {
	marks := "/-_.?=&"
	url := []byte("https://")
	host := 3 + nextRandom(seed)%8
	for i := int64(0); i < host; i++ {
		url = append(url, byte('a'+nextRandom(seed)%26))
	}
	url = append(url, ".com/"...)
	path := nextRandom(seed) % (most + 1)
	for i := int64(0); i < path; i++ {
		k := nextRandom(seed) % 69
		if k < 26 {
			url = append(url, byte('a'+k))
		} else if k < 52 {
			url = append(url, byte('A'+k-26))
		} else if k < 62 {
			url = append(url, byte('0'+k-52))
		} else {
			url = append(url, marks[k-62])
		}
	}
	return string(url)
}

func main() {
	seed := int64(535)
	urls := []string{}
	for i := 0; i < 20000; i++ {
		if i%5 == 4 {
			j := nextRandom(&seed) % int64(len(urls))
			urls = append(urls, urls[j])
		} else {
			urls = append(urls, randomURL(&seed, 100))
		}
	}
	rounds := 50
	right := 0
	length := 0
	for r := 0; r < rounds; r++ {
		codec := newCodec()
		shorts := []string{}
		for _, u := range urls {
			s := codec.encode(u)
			length += len(s)
			shorts = append(shorts, s)
		}
		for i := range urls {
			if codec.decode(shorts[i]) == urls[i] {
				right++
			}
		}
	}
	fmt.Printf("%d URLs, %d rounds: %d back, short length %d\n", len(urls), rounds, right, length)
}
