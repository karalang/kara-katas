// LeetCode #2121: Intervals Between Identical Elements -- the benchmark,
// the same algorithm as intervals.kara: each value's indices gathered in a
// hash map, then one running sum per list.

use std::collections::HashMap;

fn get_distances(arr: &[i64]) -> Vec<i64> {
    let mut positions: HashMap<i64, Vec<i64>> = HashMap::new();
    for i in 0..arr.len() {
        positions.entry(arr[i]).or_insert_with(Vec::new).push(i as i64);
    }
    let mut answer = vec![0i64; arr.len()];
    for p in positions.values() {
        let c = p.len() as i64;
        let total: i64 = p.iter().sum();
        let mut before = 0;
        for k in 0..c {
            let pk = p[k as usize];
            let after = total - before - pk;
            answer[pk as usize] = k * pk - before + after - (c - k - 1) * pk;
            before += pk;
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2121;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for g in 0..40 {
        let top = [10, 100, 1000, 10000][g % 4];
        let arr: Vec<i64> = (0..50000).map(|_| next_random(&mut seed) % top + 1).collect();
        arrays.push(arr);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..20usize {
        for g in 0..40usize {
            arrays[g][(round * 7919 + g * 104729) % 50000] += 1;
            let sum: i64 = get_distances(&arrays[g]).iter().sum();
            total += sum;
            check = (check * 31 + sum % 1000000007) % 1000000007;
        }
    }
    println!("800 solves: distances sum to {}, checksum {}", total, check);
}
