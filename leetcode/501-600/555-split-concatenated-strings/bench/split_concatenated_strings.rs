// Benchmark for #555: Rust mirror of the ★ arm (every cut, the rest at
// its best); see split_concatenated_strings.kara.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn split_loop(strs: &[String]) -> String {
    let n = strs.len();
    let mut larger: Vec<String> = Vec::new();
    for s in strs {
        let r: String = s.chars().rev().collect();
        if r > *s {
            larger.push(r);
        } else {
            larger.push(s.clone());
        }
    }
    let mut answer = String::new();
    for i in 0..n {
        let mut middle = String::new();
        for j in 1..n {
            middle.push_str(&larger[(i + j) % n]);
        }
        let backward: String = strs[i].chars().rev().collect();
        for t in [strs[i].clone(), backward] {
            for k in 0..t.len() {
                let candidate = format!("{}{}{}", &t[k..], middle, &t[..k]);
                if candidate > answer {
                    answer = candidate;
                }
            }
        }
    }
    answer
}

fn main() {
    let count = 100;
    let mut seed: i64 = 555;
    let mut lists: Vec<Vec<String>> = Vec::new();
    let mut strings = 0;
    for _ in 0..count {
        let alphabet = 2 + next_random(&mut seed) % 25;
        let mut strs: Vec<String> = Vec::new();
        let mut left = 1000;
        while left > 0 {
            let length = (1 + next_random(&mut seed) % 40).min(left);
            let mut s = String::new();
            for _ in 0..length {
                s.push((b'a' + (next_random(&mut seed) % alphabet) as u8) as char);
            }
            strs.push(s);
            left -= length;
        }
        strings += strs.len();
        lists.push(strs);
    }
    let mut checksum: i64 = 0;
    for round in 0..30 {
        for g in 0..count {
            let got = split_loop(&lists[(round * 7 + g) % count]);
            let b = got.as_bytes();
            checksum = (checksum * 31 + b.len() as i64 + b[0] as i64 * 7 + b[b.len() / 2] as i64) % 1000000007;
        }
    }
    println!("{} lists, {} strings, 30 rounds each: checksum {}", count, strings, checksum);
}
