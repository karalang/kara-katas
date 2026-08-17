// LeetCode 278 bench mirror — Rust. Build one dictionary, solve it 48 times.
const WORDS: usize = 250000;
const ALPHA: i64 = 6;
const WIDTH: usize = 8;
const INSTANCES: i64 = 48;

fn solve_len(dict: &[Vec<u8>]) -> i64 {
    let mut present = [false; 26];
    let mut indeg = [0i64; 26];
    let mut adj = vec![false; 676];
    for w in dict { for &ch in w { present[(ch - b'a') as usize] = true; } }
    for p in 0..dict.len() - 1 {
        let (a, c) = (&dict[p], &dict[p + 1]);
        let mut found = false;
        for k in 0..a.len().min(c.len()) {
            if a[k] != c[k] {
                let (u, v) = ((a[k] - b'a') as usize, (c[k] - b'a') as usize);
                if !adj[u * 26 + v] { adj[u * 26 + v] = true; indeg[v] += 1; }
                found = true;
                break;
            }
        }
        if !found && a.len() > c.len() { return 0; }
    }
    let mut done = [false; 26];
    let mut remaining = (0..26).filter(|&r| present[r]).count() as i64;
    let mut out = 0i64;
    while remaining > 0 {
        let mut pick: i64 = -1;
        for s in 0..26 { if present[s] && !done[s] && indeg[s] == 0 { pick = s as i64; break; } }
        if pick < 0 { return 0; }
        done[pick as usize] = true;
        out += 1;
        for t in 0..26 { if adj[pick as usize * 26 + t] { indeg[t] -= 1; } }
        remaining -= 1;
    }
    out
}

fn main() {
    let mut dict: Vec<Vec<u8>> = Vec::with_capacity(WORDS);
    for n in 0..WORDS {
        let mut rem = n as i64;
        let mut digits = [0i64; WIDTH];
        for pos in 0..WIDTH { digits[pos] = rem % ALPHA; rem /= ALPHA; }
        let mut w = Vec::with_capacity(WIDTH);
        for q in (0..WIDTH).rev() { w.push(b'a' + (ALPHA - 1 - digits[q]) as u8); }
        dict.push(w);
    }
    let mut sink = 0i64;
    for i in 0..INSTANCES {
        sink = (sink + (i * 1000003 + solve_len(&dict)) % 1000000007) % 1000000007;
    }
    println!("{}", sink);
}
