// LeetCode #2157: Groups of Strings -- the benchmark's Rust mirror of
// groups.kara.

use std::collections::HashMap;

fn find(parent: &mut Vec<i64>, x: i64) -> i64 {
    let mut x = x;
    while parent[x as usize] != x {
        parent[x as usize] = parent[parent[x as usize] as usize];
        x = parent[x as usize];
    }
    x
}

fn unite(parent: &mut Vec<i64>, size: &mut Vec<i64>, a: i64, b: i64) {
    let ra = find(parent, a);
    let rb = find(parent, b);
    if ra == rb {
        return;
    }
    let (big, small) = if size[ra as usize] >= size[rb as usize] { (ra, rb) } else { (rb, ra) };
    parent[small as usize] = big;
    size[big as usize] += size[small as usize];
}

fn group_strings(words: &[String]) -> Vec<i64> {
    let n = words.len();
    let masks: Vec<i64> = words.iter().map(|w| w.bytes().fold(0i64, |m, b| m | (1 << (b - b'a')))).collect();
    let mut parent: Vec<i64> = (0..n as i64).collect();
    let mut size: Vec<i64> = vec![1; n];
    let mut first: HashMap<i64, i64> = HashMap::new();
    for i in 0..n {
        match first.get(&masks[i]) {
            Some(&j) => unite(&mut parent, &mut size, i as i64, j),
            None => {
                first.insert(masks[i], i as i64);
            }
        }
    }
    let mut blanked: HashMap<i64, i64> = HashMap::new();
    for i in 0..n {
        for bit in 0..26 {
            if (masks[i] >> bit) & 1 == 1 {
                let less = masks[i] ^ (1 << bit);
                if let Some(&j) = first.get(&less) {
                    unite(&mut parent, &mut size, i as i64, j);
                }
                match blanked.get(&less) {
                    Some(&j) => unite(&mut parent, &mut size, i as i64, j),
                    None => {
                        blanked.insert(less, i as i64);
                    }
                }
            }
        }
    }
    let mut groups = 0;
    let mut largest = 0;
    for i in 0..n {
        if find(&mut parent, i as i64) == i as i64 {
            groups += 1;
            largest = largest.max(size[i]);
        }
    }
    vec![groups, largest]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(seed: &mut i64) -> String {
    let length = (next_random(seed) % 8 + 1) as usize;
    let mut w = String::new();
    while w.len() < length {
        let c = (b'a' + (next_random(seed) % 20) as u8) as char;
        if !w.contains(c) {
            w.push(c);
        }
    }
    w
}

fn main() {
    let mut seed = 2157i64;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..4 {
        let words: Vec<String> = (0..5000).map(|_| word(&mut seed)).collect();
        lists.push(words);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..25i64 {
        for l in 0..4 {
            let at = (next_random(&mut seed) % 5000) as usize;
            lists[l][at] = word(&mut seed);
            let answer = group_strings(&lists[l]);
            total += answer[0];
            check = (check * 31 + answer[0] * 10007 + answer[1] + round) % 1000000007;
        }
    }
    println!("100 solves: {} groups in all, checksum {}", total, check);
}
