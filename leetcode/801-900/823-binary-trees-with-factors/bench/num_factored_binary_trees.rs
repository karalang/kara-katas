// Benchmark for #823: Binary Trees With Factors -- the ★ arm (counts in a map).
//
// Mirrors num_factored_binary_trees.kara: sort a copy of the values, so
// that both factors of a value come before it, and count each value's
// trees from its factors' counts, looked up by value in a map.

use std::collections::HashMap;

fn num_factored_binary_trees(arr: &[i64]) -> i64 {
    let modulus = 1000000007i64;
    let mut values = arr.to_vec();
    values.sort();
    let mut trees: HashMap<i64, i64> = HashMap::new();
    let mut total = 0;
    for i in 0..values.len() {
        let x = values[i];
        let mut count = 1;
        for j in 0..i {
            let left = values[j];
            if x % left == 0 {
                if let Some(&right) = trees.get(&(x / left)) {
                    count = (count + trees[&left] * right) % modulus;
                }
            }
        }
        trees.insert(x, count);
        total = (total + count) % modulus;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let limit = 1000000000i64;
    let mut smooth: Vec<i64> = Vec::new();
    let mut p2 = 1;
    while p2 <= limit {
        let mut p3 = p2;
        while p3 <= limit {
            let mut p5 = p3;
            while p5 <= limit {
                let mut p7 = p5;
                while p7 <= limit {
                    if p7 > 1 {
                        smooth.push(p7);
                    }
                    p7 *= 7;
                }
                p5 *= 5;
            }
            p3 *= 3;
        }
        p2 *= 2;
    }
    smooth.sort();
    let count = 64usize;
    let rounds = 1000usize;
    let mut seed: i64 = 823;
    let mut sets: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut taken = vec![false; smooth.len()];
        let mut set = Vec::new();
        while set.len() < 1000 {
            let k = (next_random(&mut seed) % smooth.len() as i64) as usize;
            if !taken[k] {
                taken[k] = true;
                set.push(smooth[k]);
            }
        }
        sets.push(set);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let answer = num_factored_binary_trees(&sets[round % count]);
        total += answer;
        checksum = (checksum * 131 + answer) % 1000000007;
    }
    println!("{} values, {rounds} rounds of {count} sets: total {total}, checksum {checksum}", smooth.len());
}
