// Benchmark for #839: Similar String Groups -- the ★ arm (union-find).
//
// Mirrors similar_string_groups.kara: every pair of words is compared
// once, stopping at a third difference, and a pair that differs in no
// position or in two joins its two groups, kept as a union-find forest
// with path halving. As in the Kāra program, each word is copied out to
// its own vector for every count.

fn similar(a: &[u8], b: &[u8]) -> bool {
    let mut diff = 0;
    for k in 0..a.len() {
        if a[k] != b[k] {
            diff += 1;
            if diff > 2 {
                return false;
            }
        }
    }
    diff != 1
}

fn find(parent: &mut Vec<i64>, x: i64) -> i64 {
    let mut v = x;
    while parent[v as usize] != v {
        parent[v as usize] = parent[parent[v as usize] as usize];
        v = parent[v as usize];
    }
    v
}

fn num_similar_groups(strs: &[String]) -> i64 {
    let words: Vec<Vec<u8>> = strs.iter().map(|s| s.bytes().collect()).collect();
    let n = words.len() as i64;
    let mut parent: Vec<i64> = (0..n).collect();
    let mut groups = n;
    for i in 0..n {
        for j in i + 1..n {
            let a = find(&mut parent, i);
            let b = find(&mut parent, j);
            if a != b && similar(&words[i as usize], &words[j as usize]) {
                parent[a as usize] = b;
                groups -= 1;
            }
        }
    }
    groups
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 16 cases drawn once, each LeetCode's most and longest words, 300 of
    // 300 letters. The first word of case g is random; each later one is
    // an earlier word with one swap, or with three once in 1 + g % 4
    // words. Each round counts the groups of the next case.
    let count: i64 = 16;
    let rounds: i64 = 500;
    let n: i64 = 300;
    let m: i64 = 300;
    let mut seed: i64 = 839;
    let mut cases: Vec<Vec<String>> = Vec::new();
    for g in 0..count {
        let jump = 1 + g % 4;
        let mut words: Vec<Vec<u8>> = Vec::new();
        let mut first: Vec<u8> = Vec::new();
        for _ in 0..m {
            first.push(97 + (next_random(&mut seed) % 26) as u8);
        }
        words.push(first);
        for _ in 1..n {
            let from = next_random(&mut seed) % words.len() as i64;
            let swaps = if next_random(&mut seed) % jump == 0 { 3 } else { 1 };
            let mut w = words[from as usize].clone();
            for _ in 0..swaps {
                let p = next_random(&mut seed) % m;
                let q = next_random(&mut seed) % m;
                w.swap(p as usize, q as usize);
            }
            words.push(w);
        }
        cases.push(words.into_iter().map(|w| String::from_utf8(w).unwrap()).collect());
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let groups = num_similar_groups(&cases[(round % count) as usize]);
        total += groups;
        checksum = (checksum * 31 + groups + round) % 1000000007;
    }
    println!("{rounds} rounds of {count} cases: {total} groups, checksum {checksum}");
}
