// Benchmark: LeetCode #943 Find the Shortest Superstring -- the ★ arm,
// the most letters saved, on sets of 12 words of 20 letters, LeetCode's
// largest. Mirrors shortest_superstring.kara, .c, .py and go-seq/.

fn overlap(a: &str, b: &str) -> i64 {
    let (a, b) = (a.as_bytes(), b.as_bytes());
    let mut k = a.len().min(b.len()) as i64 - 1;
    while k > 0 {
        let ku = k as usize;
        if a[a.len() - ku..] == b[..ku] {
            return k;
        }
        k -= 1;
    }
    0
}

fn shortest_superstring(words: &[String]) -> String {
    let n = words.len();
    let mut ov = vec![0i64; n * n];
    for i in 0..n {
        for j in 0..n {
            if i != j {
                ov[i * n + j] = overlap(&words[i], &words[j]);
            }
        }
    }
    let full = (1usize << n) - 1;
    let mut saved = vec![-1i64; (full + 1) * n];
    let mut before = vec![-1i64; (full + 1) * n];
    for mask in 1..=full {
        for last in 0..n {
            if (mask >> last) & 1 == 1 {
                let rest = mask ^ (1 << last);
                if rest == 0 {
                    saved[mask * n + last] = 0;
                } else {
                    for p in 0..n {
                        if (rest >> p) & 1 == 1 {
                            let s = saved[rest * n + p] + ov[p * n + last];
                            if s > saved[mask * n + last] {
                                saved[mask * n + last] = s;
                                before[mask * n + last] = p as i64;
                            }
                        }
                    }
                }
            }
        }
    }
    let mut last: i64 = 0;
    for w in 1..n {
        if saved[full * n + w] > saved[full * n + last as usize] {
            last = w as i64;
        }
    }
    let mut order: Vec<usize> = Vec::new();
    let mut mask = full;
    while last >= 0 {
        let l = last as usize;
        order.push(l);
        let p = before[mask * n + l];
        mask ^= 1 << l;
        last = p;
    }
    let mut out = words[order[order.len() - 1]].clone();
    let mut i = order.len() - 1;
    while i > 0 {
        let (a, b) = (order[i], order[i - 1]);
        out = out + &words[b][ov[a * n + b] as usize..];
        i -= 1;
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, size, length) = (10, 40, 12, 20);
    let mut seed = 943;
    let mut sets: Vec<Vec<String>> = Vec::new();
    for _ in 0..count {
        let letters = 2 + next_random(&mut seed) % 3;
        let mut words: Vec<String> = Vec::new();
        while words.len() < size {
            let mut w = String::new();
            for _ in 0..length {
                w.push((next_random(&mut seed) % letters + 97) as u8 as char);
            }
            if !words.contains(&w) {
                words.push(w);
            }
        }
        sets.push(words);
    }
    let mut total = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let s = shortest_superstring(&sets[(r + i) % count]);
            total += s.len();
            for &c in s.as_bytes() {
                check = (check * 31 + c as i64) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over {count} sets of {size} words of {length} letters: lengths adding to {total}, checksum {check}");
}
