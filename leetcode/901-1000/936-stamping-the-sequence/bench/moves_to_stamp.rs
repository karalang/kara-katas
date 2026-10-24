// LeetCode #936: Stamping The Sequence -- bench: stamps peeled off in
// reverse. Mirrors moves_to_stamp.kara, .c, .py and go-seq/.

fn moves_to_stamp(stamp: &[u8], target: &[u8]) -> Vec<i64> {
    let s = stamp;
    let mut t = target.to_vec();
    let m = s.len();
    let n = t.len();
    let mut erased = 0;
    let mut order: Vec<i64> = Vec::new();
    let mut progress = true;
    while progress && erased < n {
        progress = false;
        for p in 0..n - m + 1 {
            let mut fits = true;
            let mut fresh = false;
            for k in 0..m {
                if t[p + k] == s[k] {
                    fresh = true;
                } else if t[p + k] != b'?' {
                    fits = false;
                }
            }
            if fits && fresh {
                for k in 0..m {
                    if t[p + k] != b'?' {
                        t[p + k] = b'?';
                        erased += 1;
                    }
                }
                order.push(p as i64);
                progress = true;
            }
        }
    }
    if erased < n {
        return Vec::new();
    }
    order.reverse();
    order
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 100;
    let count: i64 = 50;
    let n: i64 = 1000;
    let mut seed: i64 = 936;
    let mut stamps: Vec<Vec<u8>> = Vec::new();
    let mut targets: Vec<Vec<u8>> = Vec::new();
    for c in 0..count {
        let m = 5 + next_random(&mut seed) % 16;
        let mut s: Vec<u8> = Vec::new();
        for _ in 0..m {
            s.push((97 + next_random(&mut seed) % 3) as u8);
        }
        let mut out = vec![b'?'; n as usize];
        let mut left = n;
        while left > 0 {
            let p = next_random(&mut seed) % (n - m + 1);
            for k in 0..m {
                let i = (p + k) as usize;
                if out[i] == b'?' {
                    left -= 1;
                }
                out[i] = s[k as usize];
            }
        }
        if c % 2 == 1 {
            let at = next_random(&mut seed) % n;
            out[at as usize] = (97 + next_random(&mut seed) % 3) as u8;
        }
        stamps.push(s);
        targets.push(out);
    }
    let mut stamped: i64 = 0;
    let mut turns: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let c = ((r + i) % count) as usize;
            let moves = moves_to_stamp(&stamps[c], &targets[c]);
            if !moves.is_empty() {
                stamped += 1;
            }
            turns += moves.len() as i64;
            for p in &moves {
                check = (check * 1000003 + p + 1) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over {count} targets of {n} letters: {stamped} stamped, {turns} stamps, checksum {check}");
}
