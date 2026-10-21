// Benchmark for #830: Positions of Large Groups -- the ★ arm (two pointers).
//
// Mirrors large_group_positions.kara: from the start i of each group, j
// runs on while the letter stays the same, and the group s[i..j] is kept
// when it holds 3 or more.

fn large_group_positions(s: &str) -> Vec<Vec<i64>> {
    let b = s.as_bytes();
    let n = b.len();
    let mut groups: Vec<Vec<i64>> = Vec::new();
    let mut i = 0;
    while i < n {
        let mut j = i;
        while j < n && b[j] == b[i] {
            j += 1;
        }
        if j - i >= 3 {
            groups.push(vec![i as i64, j as i64 - 1]);
        }
        i = j;
    }
    groups
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64i64;
    let rounds = 200000i64;
    let n = 1000;
    let mut seed = 830i64;
    let mut strings: Vec<String> = Vec::new();
    for g in 0..count {
        let letters = 1 + g % 3;
        let mut s = String::new();
        for _ in 0..n {
            s.push((b'a' + (next_random(&mut seed) % letters) as u8) as char);
        }
        strings.push(s);
    }
    let mut total = 0i64;
    let mut checksum = 0i64;
    for round in 0..rounds {
        let groups = large_group_positions(&strings[(round % count) as usize]);
        total += groups.len() as i64;
        for g in groups.iter() {
            checksum = (checksum * 131 + g[0] * 1009 + g[1]) % 1000000007;
        }
    }
    println!("{} rounds of {} strings: {} groups, checksum {}", rounds, count, total, checksum);
}
