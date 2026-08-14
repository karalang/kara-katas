// Benchmark workload for LeetCode #269 — Alien Dictionary (Rust mirror).
// Mirrors alien.kara algorithm-for-algorithm, including the flat corpus and the
// hoisted working structures (see that file for why).

fn main() {
    let lists: i64 = 20000;
    let rounds: i64 = 60;
    let alpha: i64 = 8;

    let mut letters: Vec<i64> = Vec::new();
    let mut wstart: Vec<i64> = Vec::new();
    let mut wlen: Vec<i64> = Vec::new();
    let mut lstart: Vec<i64> = Vec::new();
    let mut lcount: Vec<i64> = Vec::new();

    let mut state: i64 = 269269;
    for _ in 0..lists {
        state = (state * 1103515245 + 12345) & 2147483647;
        let m = (state / 65536) % 5 + 2;

        let mut rank: Vec<i64> = (0..alpha).collect();
        let mut sh = alpha - 1;
        while sh > 0 {
            state = (state * 1103515245 + 12345) & 2147483647;
            let j = (state / 65536) % (sh + 1);
            rank.swap(sh as usize, j as usize);
            sh -= 1;
        }

        let mut buf: Vec<i64> = Vec::new();
        let mut st: Vec<i64> = Vec::new();
        let mut ln: Vec<i64> = Vec::new();
        for _ in 0..m {
            state = (state * 1103515245 + 12345) & 2147483647;
            let l = (state / 65536) % 4 + 1;
            st.push(buf.len() as i64);
            ln.push(l);
            for _ in 0..l {
                state = (state * 1103515245 + 12345) & 2147483647;
                buf.push((state / 65536) % alpha);
            }
        }

        let mut a = 1;
        while a < m {
            let mut b = a;
            while b > 0 {
                let (s1, n1) = (st[(b - 1) as usize], ln[(b - 1) as usize]);
                let (s2, n2) = (st[b as usize], ln[b as usize]);
                let lim = if n2 < n1 { n2 } else { n1 };
                let mut k = 0;
                let mut swap = false;
                let mut decided = false;
                while k < lim {
                    if buf[(s1 + k) as usize] != buf[(s2 + k) as usize] {
                        if rank[buf[(s1 + k) as usize] as usize] > rank[buf[(s2 + k) as usize] as usize] {
                            swap = true;
                        }
                        decided = true;
                        k = lim;
                    } else {
                        k += 1;
                    }
                }
                if !decided && n1 > n2 { swap = true; }
                if swap {
                    st.swap((b - 1) as usize, b as usize);
                    ln.swap((b - 1) as usize, b as usize);
                    b -= 1;
                } else {
                    b = 0;
                }
            }
            a += 1;
        }

        state = (state * 1103515245 + 12345) & 2147483647;
        if (state / 65536) % 2 == 0 && m >= 2 {
            state = (state * 1103515245 + 12345) & 2147483647;
            let at = (state / 65536) % (m - 1);
            st.swap(at as usize, (at + 1) as usize);
            ln.swap(at as usize, (at + 1) as usize);
        }

        lstart.push(wstart.len() as i64);
        lcount.push(m);
        for q in 0..m {
            wstart.push(letters.len() as i64);
            wlen.push(ln[q as usize]);
            for r in 0..ln[q as usize] {
                letters.push(buf[(st[q as usize] + r) as usize]);
            }
        }
    }

    let mut adj = vec![false; 676];
    let mut indeg = vec![0i64; 26];
    let mut present = vec![false; 26];
    let mut done = vec![false; 26];

    let mut sink: i64 = 0;
    for _ in 0..rounds {
        for idx in 0..lists {
            let base = lstart[idx as usize];
            let n = lcount[idx as usize];

            for c in 0..26 {
                indeg[c] = 0;
                present[c] = false;
                done[c] = false;
            }
            for e in 0..676 { adj[e] = false; }

            for w in 0..n {
                let s = wstart[(base + w) as usize];
                let l = wlen[(base + w) as usize];
                for p in 0..l {
                    present[letters[(s + p) as usize] as usize] = true;
                }
            }

            let mut bad = false;
            let mut p2 = 0i64;
            while p2 + 1 < n {
                let (s1, n1) = (wstart[(base + p2) as usize], wlen[(base + p2) as usize]);
                let (s2, n2) = (wstart[(base + p2 + 1) as usize], wlen[(base + p2 + 1) as usize]);
                let lim = if n2 < n1 { n2 } else { n1 };
                let mut k = 0;
                let mut found = false;
                while k < lim {
                    let x = letters[(s1 + k) as usize];
                    let y = letters[(s2 + k) as usize];
                    if x != y {
                        if !adj[(x * 26 + y) as usize] {
                            adj[(x * 26 + y) as usize] = true;
                            indeg[y as usize] += 1;
                        }
                        found = true;
                        k = lim;
                    } else {
                        k += 1;
                    }
                }
                if !found && n1 > n2 { bad = true; p2 = n; } else { p2 += 1; }
            }

            let mut acc: i64 = 0;
            if !bad {
                let mut remaining = 0i64;
                for d in 0..26 { if present[d] { remaining += 1; } }
                let mut placed = 0i64;
                while placed < remaining {
                    let mut pick: i64 = -1;
                    let mut s3 = 0usize;
                    while s3 < 26 {
                        if present[s3] && !done[s3] && indeg[s3] == 0 {
                            pick = s3 as i64;
                            s3 = 26;
                        } else {
                            s3 += 1;
                        }
                    }
                    if pick < 0 {
                        acc = 0;
                        placed = remaining;
                    } else {
                        done[pick as usize] = true;
                        acc = (acc * 31 + pick + 1) % 1000000007;
                        placed += 1;
                        for t in 0..26 {
                            if adj[(pick * 26 + t as i64) as usize] { indeg[t] -= 1; }
                        }
                    }
                }
            }
            sink = (sink * 131 + acc) % 1000000007;
        }
    }

    println!("{}", sink);
}
