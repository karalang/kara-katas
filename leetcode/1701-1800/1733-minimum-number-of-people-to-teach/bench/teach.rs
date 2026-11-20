// LeetCode #1733: Minimum Number of People to Teach -- the bench
// (teach.kara): the stuck users gathered in a set, and the language most
// of them know.

use std::collections::HashSet;

fn minimum_teachings(n: i32, languages: &[Vec<i32>], friendships: &[Vec<i32>]) -> i32 {
    let known: Vec<HashSet<i32>> = languages
        .iter()
        .map(|l| l.iter().cloned().collect())
        .collect();
    let mut stuck: HashSet<usize> = HashSet::new();
    for f in friendships.iter() {
        let (u, v) = (f[0] as usize - 1, f[1] as usize - 1);
        if known[u].is_disjoint(&known[v]) {
            stuck.insert(u);
            stuck.insert(v);
        }
    }
    let mut speakers = vec![0i32; n as usize + 1];
    for &u in stuck.iter() {
        for &l in known[u].iter() {
            speakers[l as usize] += 1;
        }
    }
    stuck.len() as i32 - *speakers.iter().max().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let rounds: i64 = 200;
    let (n, users, pairs): (i64, usize, usize) = (500, 500, 500);
    let mut seed: i64 = 1733;
    let mut problems: Vec<(Vec<Vec<i32>>, Vec<Vec<i32>>)> = Vec::new();
    for _ in 0..count {
        let mut languages: Vec<Vec<i32>> = Vec::new();
        for _ in 0..users {
            let k = (next_random(&mut seed) % 10 + 1) as usize;
            let mut known: Vec<i32> = Vec::new();
            while known.len() < k {
                let l = (next_random(&mut seed) % n + 1) as i32;
                if !known.contains(&l) {
                    known.push(l);
                }
            }
            languages.push(known);
        }
        let mut friends = vec![vec![false; users]; users];
        let mut friendships: Vec<Vec<i32>> = Vec::new();
        while friendships.len() < pairs {
            let u = (next_random(&mut seed) % users as i64) as usize;
            let v = (next_random(&mut seed) % users as i64) as usize;
            if u != v && !friends[u][v] {
                friends[u][v] = true;
                friends[v][u] = true;
                friendships.push(vec![(u + 1) as i32, (v + 1) as i32]);
            }
        }
        problems.push((languages, friendships));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (languages, friendships) in problems.iter() {
            let answer = minimum_teachings(n as i32, languages, friendships) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!(
        "{} problems of {} users, {} languages and {} friendships, {} rounds: teachings sum to {}, checksum {}",
        count, users, n, pairs, rounds, sum, check
    );
}
