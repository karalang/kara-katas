// LeetCode #1152 bench -- mirrors most_visited_pattern.kara: the same
// 64 problems, the same rounds, the ★ arm's maps and sets.

use std::collections::{HashMap, HashSet};

fn most_visited_pattern(username: &[String], timestamp: &[i64], website: &[String]) -> Vec<String> {
    let mut order: Vec<usize> = (0..username.len()).collect();
    order.sort_by_key(|&i| timestamp[i]);
    let mut by_user: HashMap<String, Vec<String>> = HashMap::new();
    for &i in order.iter() {
        by_user.entry(username[i].clone()).or_insert_with(Vec::new).push(website[i].clone());
    }
    let mut score: HashMap<(String, String, String), i64> = HashMap::new();
    for (_, sites) in by_user.iter() {
        let n = sites.len();
        let mut seen: HashSet<(String, String, String)> = HashSet::new();
        for a in 0..n {
            for b in a + 1..n {
                for c in b + 1..n {
                    seen.insert((sites[a].clone(), sites[b].clone(), sites[c].clone()));
                }
            }
        }
        for p in seen.into_iter() {
            let s = score.get(&p).copied().unwrap_or(0) + 1;
            score.insert(p, s);
        }
    }
    let mut best: Option<((String, String, String), i64)> = None;
    for (p, &s) in score.iter() {
        let better = match &best {
            None => true,
            Some((q, t)) => s > *t || (s == *t && p < q),
        };
        if better {
            best = Some((p.clone(), s));
        }
    }
    let ((a, b, c), _) = best.unwrap();
    vec![a, b, c]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 5000;
    let site_names: Vec<String> = (0..8).map(|s| format!("site{}", s)).collect();
    let mut seed = 1152;
    let mut problems: Vec<(Vec<String>, Vec<i64>, Vec<String>)> = Vec::new();
    for _ in 0..64 {
        let username: Vec<String> = (0..50).map(|_| format!("user{}", next_random(&mut seed) % 5)).collect();
        let website: Vec<String> = (0..50).map(|_| site_names[(next_random(&mut seed) % 8) as usize].clone()).collect();
        let mut timestamp: Vec<i64> = (1..51).collect();
        for j in (1..50usize).rev() {
            let k = (next_random(&mut seed) % (j as i64 + 1)) as usize;
            timestamp.swap(j, k);
        }
        problems.push((username, timestamp, website));
    }
    let mut distinct = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let p = r % 64;
        for _ in 0..4 {
            let at = (next_random(&mut seed) % 50) as usize;
            problems[p].2[at] = site_names[(next_random(&mut seed) % 8) as usize].clone();
        }
        let (username, timestamp, website) = &problems[p];
        let answer = most_visited_pattern(username, timestamp, website);
        if answer[0] != answer[1] && answer[1] != answer[2] && answer[0] != answer[2] {
            distinct += 1;
        }
        for w in answer.iter() {
            for &c in w.as_bytes() {
                check = (check * 31 + c as i64) % 1000000007;
            }
        }
    }
    println!("{} rounds over 64 problems of 50 visits: {} patterns of three sites, checksum {}", rounds, distinct, check);
}
