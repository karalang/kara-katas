// LeetCode #952 bench: Rust mirror of largest_component_size.kara (the ★
// arm, union by prime, a HashMap from prime to its first place) on the
// same 20 sets.
use std::collections::HashMap;
use std::collections::HashSet;

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut root = x;
    while parent[root as usize] != root {
        root = parent[root as usize];
    }
    let mut y = x;
    while parent[y as usize] != root {
        let next = parent[y as usize];
        parent[y as usize] = root;
        y = next;
    }
    root
}

fn largest_component_size(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut parent: Vec<i64> = (0..n as i64).collect();
    let mut size: Vec<i64> = vec![1; n];
    let mut first: HashMap<i64, i64> = HashMap::new();
    for i in 0..n {
        let mut x = nums[i];
        let mut p = 2;
        while x > 1 {
            if p * p > x {
                p = x;
            }
            if x % p == 0 {
                while x % p == 0 {
                    x /= p;
                }
                match first.get(&p) {
                    Some(&j) => {
                        let a = find(&mut parent, i as i64) as usize;
                        let b = find(&mut parent, j) as usize;
                        if a != b {
                            if size[a] < size[b] {
                                parent[a] = b as i64;
                                size[b] += size[a];
                            } else {
                                parent[b] = a as i64;
                                size[a] += size[b];
                            }
                        }
                    }
                    None => {
                        first.insert(p, i as i64);
                    }
                }
            }
            p += 1;
        }
    }
    let mut best = 0;
    for i in 0..n {
        if parent[i] == i as i64 && size[i] > best {
            best = size[i];
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 40;
    let count = 20;
    let n = 2000;
    let mut seed = 952;
    // 20 sets of 2000 distinct numbers from 1 to 100000
    let mut sets: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut taken: HashSet<i64> = HashSet::new();
        let mut nums: Vec<i64> = Vec::new();
        while nums.len() < n {
            let hi = next_random(&mut seed);
            let v = 1 + (hi * 32768 + next_random(&mut seed)) % 100000;
            if taken.insert(v) {
                nums.push(v);
            }
        }
        sets.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let k = (r + i) % count;
            let size = largest_component_size(&sets[k]);
            total += size;
            check = (check * 31 + size) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} sets of {n} numbers up to 100000: largest components adding to {total}, checksum {check}");
}
