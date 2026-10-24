// LeetCode #955: Delete Columns to Make Sorted II -- Rust mirror of the
// Kara bench program (pairs settled).

fn min_deletion_size(strs: &[String]) -> i64 {
    let n = strs.len();
    let m = strs[0].len();
    let mut settled = vec![false; n];
    let mut deleted = 0;
    for c in 0..m {
        let mut breaks = false;
        for i in 0..n - 1 {
            if !settled[i] && strs[i].as_bytes()[c] > strs[i + 1].as_bytes()[c] {
                breaks = true;
                break;
            }
        }
        if breaks {
            deleted += 1;
            continue;
        }
        for i in 0..n - 1 {
            if strs[i].as_bytes()[c] < strs[i + 1].as_bytes()[c] {
                settled[i] = true;
            }
        }
    }
    deleted
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 120;
    let count = 200;
    let n = 100;
    let m = 100;
    let mut seed = 955i64;
    let mut sets: Vec<Vec<String>> = Vec::new();
    for s in 0..count {
        let letters = 2 + (s % 3) as i64;
        let mut strs: Vec<String> = Vec::new();
        for _ in 0..n {
            let mut w = String::new();
            for _ in 0..m {
                w.push((b'a' + (next_random(&mut seed) % letters) as u8) as char);
            }
            strs.push(w);
        }
        let p = s % 12;
        strs.sort_by_key(|w| w[..p].to_string());
        sets.push(strs);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for i in 0..count {
            let k = (r + i) % count;
            let d = min_deletion_size(&sets[k]);
            total += d;
            check = (check * 31 + d) % 1000000007;
        }
    }
    println!("{} rounds over {} sets of {} strings of {} letters: {} columns deleted, checksum {}", rounds, count, n, m, total, check);
}
