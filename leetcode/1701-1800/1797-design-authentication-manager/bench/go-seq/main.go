// LeetCode #1797: Design Authentication Manager -- the bench in Go: the ★
// arm, a map from each token to the second it expires, over 50 random
// scripts of 2000 calls built once, 2000 runs.
package main

import "fmt"

type authenticationManager struct {
	ttl    int32
	expiry map[string]int32
}

func newAuthenticationManager(timeToLive int32) *authenticationManager {
	return &authenticationManager{ttl: timeToLive, expiry: map[string]int32{}}
}

func (m *authenticationManager) generate(tokenID string, currentTime int32) {
	m.expiry[tokenID] = currentTime + m.ttl
}

func (m *authenticationManager) renew(tokenID string, currentTime int32) {
	if e, ok := m.expiry[tokenID]; ok && e > currentTime {
		m.expiry[tokenID] = currentTime + m.ttl
	}
}

func (m *authenticationManager) countUnexpiredTokens(currentTime int32) int32 {
	var n int32
	for _, e := range m.expiry {
		if e > currentTime {
			n++
		}
	}
	return n
}

var seed int64 = 1797

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func name(k int64) string {
	s := []byte{}
	for {
		s = append(s, "abcdefghijklmnopqrstuvwxyz"[k%26])
		k /= 26
		if k == 0 {
			return string(s)
		}
	}
}

type call struct {
	op    int64
	token string
	t     int32
}

type script struct {
	ttl   int32
	calls []call
}

func main() {
	scripts := make([]script, 0, 50)
	for i := 0; i < 50; i++ {
		ttl := 1 + nextRandom()%100000
		calls := make([]call, 0, 2000)
		var made, now int64
		for j := 0; j < 2000; j++ {
			now += 1 + nextRandom()%100
			pick := nextRandom() % 10
			if pick < 4 {
				calls = append(calls, call{0, name(made), int32(now)})
				made++
			} else if pick < 8 {
				calls = append(calls, call{1, name(nextRandom() % (made + 2)), int32(now)})
			} else {
				calls = append(calls, call{2, "", int32(now)})
			}
		}
		scripts = append(scripts, script{int32(ttl), calls})
	}
	var check int64
	for run := int64(0); run < 2000; run++ {
		s := scripts[(check+run)%50]
		m := newAuthenticationManager(s.ttl)
		for _, c := range s.calls {
			switch c.op {
			case 0:
				m.generate(c.token, c.t)
			case 1:
				m.renew(c.token, c.t)
			default:
				check = (check*31 + int64(m.countUnexpiredTokens(c.t))) % 1000000007
			}
		}
	}
	fmt.Printf("2000 runs over 50 scripts of 2000 calls: checksum %d\n", check)
}
