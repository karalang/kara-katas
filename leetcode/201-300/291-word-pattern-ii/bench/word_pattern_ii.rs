// Benchmark harness for LeetCode #291 — Word Pattern II backtracking.
// Mirrors word_pattern_ii.kara algorithm-for-algorithm.

use std::collections::{HashMap, HashSet};

fn matches(
    p: &str,
    pi: usize,
    s: &str,
    si: usize,
    map: &mut HashMap<String, String>,
    used: &mut HashSet<String>,
) -> bool {
    if pi >= p.len() {
        return si >= s.len();
    }
    if si >= s.len() {
        return false;
    }

    let key = &p[pi..pi + 1];
    // Cloned so no borrow of `map` is held across the recursive &mut call —
    // the Kara version's `match map.get(key)` binds a copy for the same reason.
    if let Some(bound) = map.get(key).cloned() {
        let blen = bound.len();
        if si + blen > s.len() {
            return false;
        }
        if &s[si..si + blen] != bound.as_str() {
            return false;
        }
        return matches(p, pi + 1, s, si + blen, map, used);
    }

    let mut end = si + 1;
    while end <= s.len() {
        let cand = &s[si..end];
        if !used.contains(cand) {
            map.insert(key.to_string(), cand.to_string());
            used.insert(cand.to_string());
            if matches(p, pi + 1, s, end, map, used) {
                return true;
            }
            map.remove(key);
            used.remove(cand);
        }
        end += 1;
    }
    false
}

fn word_pattern_match(p: &str, s: &str) -> bool {
    let mut map: HashMap<String, String> = HashMap::new();
    let mut used: HashSet<String> = HashSet::new();
    matches(p, 0, s, 0, &mut map, &mut used)
}

fn main() {
    let np: usize = 8;
    let sl: usize = 30;
    let iters: usize = 500;

    let alpha = ["a", "b", "c", "d"];
    let mut subjects: Vec<String> = Vec::new();
    for j in 0..np {
        let mut sj = String::new();
        for k in 0..sl {
            let kk = if j % 2 == 0 { k % (sl / 2) } else { k };
            sj.push_str(alpha[(kk * 7 + j * 3) % 4]);
        }
        subjects.push(sj);
    }

    let pat = "abcabc";
    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = (it * 5) % np;
        if word_pattern_match(pat, &subjects[idx]) {
            sink += it as i64 + 1;
        } else {
            sink += 1;
        }
    }
    println!("{}", sink);
}
