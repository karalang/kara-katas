// LeetCode #1472: Design Browser History -- bench, Go mirror of
// browser_history.kara
package main

import "fmt"

type BrowserHistory struct {
	pages   []string
	at, end int64
}

func newHistory(homepage string) *BrowserHistory {
	return &BrowserHistory{pages: []string{homepage}, at: 0, end: 1}
}

func (h *BrowserHistory) visit(url string) {
	h.at++
	if h.at < int64(len(h.pages)) {
		h.pages[h.at] = url
	} else {
		h.pages = append(h.pages, url)
	}
	h.end = h.at + 1
}

func (h *BrowserHistory) back(steps int32) string {
	h.at = max(h.at-int64(steps), 0)
	return h.pages[h.at]
}

func (h *BrowserHistory) forward(steps int32) string {
	h.at = min(h.at+int64(steps), h.end-1)
	return h.pages[h.at]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func fold(check int64, url string) int64 {
	for i := 0; i < len(url); i++ {
		check = (check*131 + int64(url[i])) % 1000000007
	}
	return check
}

func main() {
	pool := make([]string, 1000)
	for i := range pool {
		pool[i] = fmt.Sprintf("site%d.example.com", i)
	}
	seed, check := int64(1472), int64(0)
	for s := 0; s < 400; s++ {
		h := newHistory("home.example.com")
		for c := 0; c < 5000; c++ {
			r := nextRandom(&seed) % 3
			x := nextRandom(&seed)
			if r == 0 {
				h.visit(pool[x%1000])
			} else if r == 1 {
				check = fold(check, h.back(int32(1+x%10)))
			} else {
				check = fold(check, h.forward(int32(1+x%10)))
			}
		}
	}
	fmt.Printf("400 sessions of 5000 calls: checksum %d\n", check)
}
