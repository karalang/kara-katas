// LeetCode #1788: Maximize the Beauty of the Garden -- the bench in Rust,
// mirroring maximum_beauty.kara: a prefix sum of the positives and each
// beauty's first position.
use std::collections::HashMap;

fn maximum_beauty(flowers: &[i32]) -> i32 {
    let n = flowers.len();
    let mut positive: Vec<i64> = vec![0; n + 1];
    for i in 0..n {
        positive[i + 1] = positive[i] + flowers[i].max(0) as i64;
    }
    let mut first: HashMap<i32, usize> = HashMap::new();
    let mut best = i64::MIN;
    for j in 0..n {
        let v = flowers[j];
        match first.get(&v) {
            Some(&i) => {
                let garden = 2 * v as i64 + positive[j] - positive[i + 1];
                best = best.max(garden);
            }
            None => {
                first.insert(v, j);
            }
        }
    }
    best as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1788;
    let mut gardens: Vec<Vec<i32>> = Vec::new();
    for _ in 0..400 {
        let mut flowers: Vec<i32> = Vec::new();
        for _ in 0..2000 {
            flowers.push((next_random(&mut seed) % 20001 - 10000) as i32);
        }
        flowers[1999] = flowers[0];
        gardens.push(flowers);
    }
    let mut check: i64 = 0;
    for call in 0..10000i64 {
        let flowers = &gardens[((check + call) % 400) as usize];
        check = (check * 31 + maximum_beauty(flowers) as i64 + 1000000000) % 1000000007;
    }
    println!("10000 calls over 400 gardens: checksum {}", check);
}
