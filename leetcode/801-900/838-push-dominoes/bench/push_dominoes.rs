// Benchmark for #838: Push Dominoes -- the ★ arm (the stretches between pushes).
//
// Mirrors push_dominoes.kara: the walk goes from push to push, with an L
// imagined before the line and an R after it. Between two pushes the same
// way every domino falls that way; between an R and an L the two halves
// fall inward.

fn push_dominoes(dominoes: &str) -> String {
    let mut d: Vec<char> = dominoes.chars().collect();
    let n = d.len() as i64;
    let mut left: i64 = -1;
    let mut left_push = 'L';
    for right in 0..n + 1 {
        let right_push = if right == n { 'R' } else { d[right as usize] };
        if right_push == '.' {
            continue;
        }
        if left_push == right_push {
            for i in left + 1..right {
                d[i as usize] = right_push;
            }
        } else if left_push == 'R' {
            let mut i = left + 1;
            let mut j = right - 1;
            while i < j {
                d[i as usize] = 'R';
                d[j as usize] = 'L';
                i += 1;
                j -= 1;
            }
        }
        left = right;
        left_push = right_push;
    }
    let mut out = String::new();
    for c in d {
        out.push(c);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 16 lines drawn once, each of LeetCode's longest, 10^5 dominoes,
    // line g pushing each domino left with chance 1 + 4g in 200 and right
    // with the same chance. Each round settles the next line and reads 16
    // dominoes of the result.
    let count: i64 = 16;
    let rounds: i64 = 1300;
    let n: i64 = 100000;
    let mut seed: i64 = 838;
    let mut lines: Vec<String> = Vec::new();
    for g in 0..count {
        let pushed = 1 + 4 * g;
        let mut s = String::new();
        for _ in 0..n {
            let r = next_random(&mut seed) % 200;
            s.push(if r < pushed { 'L' } else if r < 2 * pushed { 'R' } else { '.' });
        }
        lines.push(s);
    }
    let mut fallen: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let out = push_dominoes(&lines[(round % count) as usize]);
        let bytes = out.as_bytes();
        for t in 0..16 {
            let b = bytes[((round * 7919 + t * 6151) % n) as usize] as i64;
            if b != 46 {
                fallen += 1;
            }
            checksum = (checksum * 31 + b) % 1000000007;
        }
    }
    println!("{} rounds of {} lines: {} of the dominoes read fallen, checksum {}", rounds, count, fallen, checksum);
}
