// LeetCode #1061: Lexicographically Smallest Equivalent String -- the
// benchmark, the same union-find as lexi.kara.

fn find(parent: &mut [i64; 26], x: i64) -> i64 {
    let mut root = x;
    while parent[root as usize] != root {
        root = parent[root as usize];
    }
    let mut y = x;
    while parent[y as usize] != root {
        let next = parent[y as usize];
        parent[y as usize] = root;
        y = next;
    }
    root
}

fn smallest_equivalent(s1: &str, s2: &str, base: &str) -> String {
    let mut parent: [i64; 26] = [0; 26];
    for (i, p) in parent.iter_mut().enumerate() {
        *p = i as i64;
    }
    for (a, b) in s1.bytes().zip(s2.bytes()) {
        let ra = find(&mut parent, (a - b'a') as i64);
        let rb = find(&mut parent, (b - b'a') as i64);
        if ra < rb {
            parent[rb as usize] = ra;
        } else {
            parent[ra as usize] = rb;
        }
    }
    let mut out = String::new();
    for c in base.bytes() {
        let root = find(&mut parent, (c - b'a') as i64);
        out.push((b'a' + root as u8) as char);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(n: i64, k: i64, seed: &mut i64) -> String {
    let mut s = String::new();
    for _ in 0..n {
        s.push((b'a' + (next_random(seed) % k) as u8) as char);
    }
    s
}

fn main() {
    let mut seed = 1061;
    let mut s1s = Vec::new();
    let mut s2s = Vec::new();
    for p in 0..100 {
        let k = 2 + p % 25;
        s1s.push(random_word(1000, k, &mut seed));
        s2s.push(random_word(1000, k, &mut seed));
    }
    let mut bases = Vec::new();
    for _ in 0..100 {
        bases.push(random_word(20000, 26, &mut seed));
    }
    let mut calls: i64 = 0;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for p in 0..100 {
        for b in 0..100 {
            let answer = smallest_equivalent(&s1s[p], &s2s[p], &bases[b]);
            let mut sum: i64 = 0;
            for c in answer.bytes() {
                sum += c as i64;
            }
            total += sum;
            check = (check * 31 + sum % 1000003) % 1000000007;
            calls += 1;
        }
    }
    println!("{} calls: letters sum {}, checksum {}", calls, total, check);
}
