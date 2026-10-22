// Benchmark for #857: Minimum Cost to Hire K Workers -- the ★ arm,
// mirroring mincost_to_hire_workers.kara.
use std::collections::BinaryHeap;

fn mincost_to_hire_workers(quality: &[i64], wage: &[i64], k: i64) -> f64 {
    let n = quality.len();
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by(|&a, &b| (wage[a] * quality[b]).cmp(&(wage[b] * quality[a])));
    let mut heap: BinaryHeap<i64> = BinaryHeap::new();
    let mut sum = 0;
    let mut best_num: i64 = -1;
    let mut best_den: i64 = 1;
    for &i in order.iter() {
        heap.push(quality[i]);
        sum += quality[i];
        if heap.len() as i64 > k {
            sum -= heap.pop().unwrap();
        }
        if heap.len() as i64 == k {
            let num = wage[i] * sum;
            let den = quality[i];
            if best_num < 0 || num * best_den < best_num * den {
                best_num = num;
                best_den = den;
            }
        }
    }
    best_num as f64 / best_den as f64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 16;
    let rounds = 600;
    let n = 10000;
    let mut seed: i64 = 857;
    let mut qualities: Vec<Vec<i64>> = Vec::new();
    let mut wages: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut quality = Vec::new();
        let mut wage = Vec::new();
        for _ in 0..n {
            quality.push(1 + next_random(&mut seed) % 10000);
            wage.push(1 + next_random(&mut seed) % 10000);
        }
        qualities.push(quality);
        wages.push(wage);
    }
    let mut total = 0.0;
    for round in 0..rounds {
        let g = round % count;
        total += mincost_to_hire_workers(&qualities[g], &wages[g], 1 + g as i64 * 600);
    }
    println!("{} rounds of 16 sets: costs sum to {:.5}", rounds, total);
}
