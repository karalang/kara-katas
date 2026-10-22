// Benchmark for #844: Backspace String Compare -- Rust twin of the Kāra ★
// arm (two pointers from the back).

// the index of the last surviving character at or before `i`, or -1
fn next_kept(s: &[u8], i: i64) -> i64 {
    let mut i = i;
    let mut skip = 0;
    while i >= 0 {
        if s[i as usize] == b'#' {
            skip += 1;
        } else if skip > 0 {
            skip -= 1;
        } else {
            return i;
        }
        i -= 1;
    }
    -1
}

fn backspace_compare(s: &str, t: &str) -> bool {
    let a = s.as_bytes();
    let b = t.as_bytes();
    let mut i = next_kept(a, a.len() as i64 - 1);
    let mut j = next_kept(b, b.len() as i64 - 1);
    while i >= 0 && j >= 0 {
        if a[i as usize] != b[j as usize] {
            return false;
        }
        i = next_kept(a, i - 1);
        j = next_kept(b, j - 1);
    }
    i < 0 && j < 0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64usize;
    let rounds = 3500000usize;
    let mut seed: i64 = 844;
    let mut firsts: Vec<String> = Vec::new();
    let mut seconds: Vec<String> = Vec::new();
    for g in 0..count {
        let k = 2 + (g % 3) as i64;
        let mut cs: Vec<char> = Vec::new();
        for _ in 0..120 {
            if next_random(&mut seed) % 10 < 3 {
                cs.push('#');
            } else {
                cs.push((97 + next_random(&mut seed) % k) as u8 as char);
            }
        }
        let first: String = cs.iter().collect();
        for _ in 0..40 {
            let at = (next_random(&mut seed) % (cs.len() as i64 + 1)) as usize;
            cs.insert(at, '#');
            cs.insert(at, (97 + next_random(&mut seed) % k) as u8 as char);
        }
        if g % 2 == 1 {
            let at = (next_random(&mut seed) % cs.len() as i64) as usize;
            cs[at] = if cs[at] == '#' { 'a' } else { '#' };
        }
        let second: String = cs.iter().collect();
        firsts.push(first);
        seconds.push(second);
    }
    let mut equal = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = round % count;
        let same = backspace_compare(&firsts[g], &seconds[g]);
        if same {
            equal += 1;
        }
        checksum = (checksum * 31 + if same { (round % 1000) as i64 } else { 7 }) % 1000000007;
    }
    println!("{rounds} rounds of {count} pairs: {equal} equal, checksum {checksum}");
}
