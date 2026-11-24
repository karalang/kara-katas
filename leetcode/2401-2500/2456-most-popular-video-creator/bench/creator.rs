// LeetCode #2456: Most Popular Video Creator -- bench, Rust mirror of
// creator.kara: one pass keeps each creator's total and best video in a
// HashMap, then every creator at the largest total, sorted.

use std::collections::HashMap;

fn most_popular_creator(creators: &[String], ids: &[String], views: &[i64]) -> Vec<Vec<String>> {
    let mut stats: HashMap<String, (i64, i64, String)> = HashMap::new();
    for i in 0..creators.len() {
        let c = creators[i].clone();
        let next = match stats.get(&c) {
            Some((total, top, id)) => {
                let better = views[i] > *top || (views[i] == *top && ids[i] < *id);
                if better {
                    (total + views[i], views[i], ids[i].clone())
                } else {
                    (total + views[i], *top, id.clone())
                }
            }
            None => (views[i], views[i], ids[i].clone()),
        };
        stats.insert(c, next);
    }
    let mut most = 0;
    for (total, _, _) in stats.values() {
        most = most.max(*total);
    }
    let mut answer: Vec<Vec<String>> = Vec::new();
    for (c, (total, _, id)) in stats.iter() {
        if *total == most {
            answer.push(vec![c.clone(), id.clone()]);
        }
    }
    answer.sort();
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_name(len: i64, letters: i64, seed: &mut i64) -> String {
    let bytes: Vec<u8> = (0..len).map(|_| (97 + next_random(seed) % letters) as u8).collect();
    String::from_utf8(bytes).unwrap()
}

fn main() {
    let mut seed: i64 = 2456;
    let mut lists: Vec<(Vec<String>, Vec<String>, Vec<i64>)> = Vec::new();
    for _ in 0..10 {
        let creators: Vec<String> = (0..100000).map(|_| random_name(3, 26, &mut seed)).collect();
        let ids: Vec<String> = (0..100000).map(|_| random_name(5, 26, &mut seed)).collect();
        let views: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) % 100001).collect();
        lists.push((creators, ids, views));
    }
    let mut check: i64 = 0;
    for p in 0..16i64 {
        for a in 0..10usize {
            lists[a].2[((p * 7919 + a as i64) % 100000) as usize] = check % 100001;
            for pair in most_popular_creator(&lists[a].0, &lists[a].1, &lists[a].2) {
                for w in pair.iter() {
                    for b in w.bytes() {
                        check = (check * 31 + b as i64) % 1000000007;
                    }
                }
            }
            check = (check + p) % 1000000007;
        }
    }
    println!("16 passes over 10 lists of 10^5 videos: checksum {}", check);
}
