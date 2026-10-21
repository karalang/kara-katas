// Benchmark for #821: Shortest Distance to a Character -- the ★ arm (two sweeps).
//
// Mirrors shortest_to_char.kara: collect the characters, then a sweep
// from the left keeps the last `c` seen and a sweep from the right the
// first, and each place keeps the nearer of the two.

fn shortest_to_char(s: &str, c: char) -> Vec<i64> {
    let chars: Vec<char> = s.chars().collect();
    let n = chars.len() as i64;
    let mut answer = vec![0i64; n as usize];
    let mut last = -n;
    for i in 0..n {
        if chars[i as usize] == c {
            last = i;
        }
        answer[i as usize] = i - last;
    }
    last = 2 * n;
    for i in (0..n).rev() {
        if chars[i as usize] == c {
            last = i;
        }
        answer[i as usize] = answer[i as usize].min(last - i);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64usize;
    let rounds = 50000usize;
    let mut seed: i64 = 821;
    let mut strings: Vec<String> = Vec::new();
    let mut targets: Vec<char> = Vec::new();
    for _ in 0..count {
        let mut s = String::new();
        for _ in 0..10000 {
            s.push((b'a' + (next_random(&mut seed) % 26) as u8) as char);
        }
        strings.push(s);
        targets.push((b'a' + (next_random(&mut seed) % 26) as u8) as char);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = round % count;
        let answer = shortest_to_char(&strings[g], targets[g]);
        for d in &answer {
            total += d;
        }
        checksum = (checksum * 131 + answer[round % 10000]) % 1000000007;
    }
    println!("{rounds} rounds of {count} strings: total {total}, checksum {checksum}");
}
