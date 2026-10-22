// Benchmark for #842: Split Array into Fibonacci Sequence -- Rust twin of
// the Kāra ★ arm (the first two numbers decide the rest).

fn read(d: &[u8], start: usize, len: usize) -> i64 {
    if len > 1 && d[start] == b'0' {
        return -1;
    }
    let mut value: i64 = 0;
    for k in start..start + len {
        value = value * 10 + (d[k] - b'0') as i64;
    }
    if value > 2147483647 { -1 } else { value }
}

fn split_into_fibonacci(num: &str) -> Vec<i64> {
    let d = num.as_bytes();
    let n = d.len();
    for i in 1..11 {
        for j in 1..11 {
            if i + j >= n {
                break;
            }
            let a = read(d, 0, i);
            let b = read(d, i, j);
            if a < 0 || b < 0 {
                continue;
            }
            let mut seq = vec![a, b];
            let mut pos = i + j;
            while pos < n {
                let c = seq[seq.len() - 1] + seq[seq.len() - 2];
                if c > 2147483647 {
                    break;
                }
                let digits = c.to_string();
                let digits = digits.as_bytes();
                if pos + digits.len() > n {
                    break;
                }
                if &d[pos..pos + digits.len()] != digits {
                    break;
                }
                seq.push(c);
                pos += digits.len();
            }
            if pos == n {
                return seq;
            }
        }
    }
    Vec::new()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64usize;
    let rounds = 240000usize;
    let mut seed: i64 = 842;
    let mut cases: Vec<String> = Vec::new();
    for g in 0..count {
        let top = [10, 1000, 100000][g % 3];
        let mut x = next_random(&mut seed) % top;
        let mut y = next_random(&mut seed) % top;
        let mut s = format!("{x}{y}");
        loop {
            let z = x + y;
            let w = z.to_string();
            if z > 2147483647 || s.len() + w.len() > 200 {
                break;
            }
            s.push_str(&w);
            x = y;
            y = z;
        }
        if g % 4 == 3 {
            let mut d = s.into_bytes();
            let at = (next_random(&mut seed) % d.len() as i64) as usize;
            d[at] = b'0' + (d[at] - b'0' + 1) % 10;
            s = String::from_utf8(d).unwrap();
        }
        cases.push(s);
    }
    let mut split = 0i64;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let seq = split_into_fibonacci(&cases[round % count]);
        if !seq.is_empty() {
            split += 1;
            checksum = (checksum * 31 + seq.len() as i64 * 1000 + seq[seq.len() - 1] % 1000) % 1000000007;
        } else {
            checksum = (checksum * 31 + 7) % 1000000007;
        }
    }
    println!("{rounds} rounds of {count} strings: {split} split, checksum {checksum}");
}
