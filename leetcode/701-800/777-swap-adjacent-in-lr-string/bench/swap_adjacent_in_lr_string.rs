// Benchmark for #777: Swap Adjacent in LR String -- mirror of the ★ arm
// (two pointers), with the same workload as the Kāra program.

fn can_transform(start: &str, end: &str) -> bool {
    let s = start.as_bytes();
    let e = end.as_bytes();
    let n = s.len();
    if e.len() != n {
        return false;
    }
    let mut i = 0;
    let mut j = 0;
    loop {
        while i < n && s[i] == b'X' {
            i += 1;
        }
        while j < n && e[j] == b'X' {
            j += 1;
        }
        if i == n || j == n {
            return i == n && j == n;
        }
        if s[i] != e[j] {
            return false;
        }
        if s[i] == b'L' && i < j {
            return false;
        }
        if s[i] == b'R' && i > j {
            return false;
        }
        i += 1;
        j += 1;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: usize = 64;
    let n: usize = 10000;
    let mut seed: i64 = 777;
    let mut starts: Vec<String> = Vec::new();
    let mut ends: Vec<String> = Vec::new();
    for g in 0..count {
        let mut s: Vec<u8> = Vec::new();
        for _ in 0..n {
            let r = next_random(&mut seed) % 4;
            s.push(if r < 2 { b'X' } else if r == 2 { b'L' } else { b'R' });
        }
        let mut e = s.clone();
        if g % 4 < 2 {
            for _ in 0..100000 {
                let i = (next_random(&mut seed) % (n as i64 - 1)) as usize;
                if (e[i] == b'X' && e[i + 1] == b'L') || (e[i] == b'R' && e[i + 1] == b'X') {
                    e.swap(i, i + 1);
                }
            }
        } else {
            let mut k = if g % 4 == 2 { n - 2 } else { (next_random(&mut seed) % (n as i64 - 1)) as usize };
            while !(e[k] == b'X' && e[k + 1] == b'R') {
                k = if k == 0 { n - 2 } else { k - 1 };
            }
            e.swap(k, k + 1);
        }
        starts.push(String::from_utf8(s).unwrap());
        ends.push(String::from_utf8(e).unwrap());
    }
    let mut yes = 0;
    let mut checksum: i64 = 0;
    for round in 0..20000 {
        let g = (round * 7) % count;
        if can_transform(&starts[g], &ends[g]) {
            yes += 1;
            checksum = (checksum * 31 + g as i64 + 1) % 1000000007;
        } else {
            checksum = (checksum * 31 + 7) % 1000000007;
        }
    }
    println!("20000 rounds of {} letters: {} reachable, checksum {}", n, yes, checksum);
}
