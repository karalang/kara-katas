// Benchmark for #781: Rabbits in Forest -- mirror of the ★ arm (groups
// counted by answer), with the same workload as the Kāra program.
use std::collections::HashMap;

fn num_rabbits(answers: &[i64]) -> i64 {
    let mut count: HashMap<i64, i64> = HashMap::new();
    for &a in answers {
        *count.entry(a).or_insert(0) += 1;
    }
    let mut total = 0;
    for (&v, &c) in count.iter() {
        let size = v + 1;
        total += (c + size - 1) / size * size;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let mut seed: i64 = 781;
    let mut forests: Vec<Vec<i64>> = Vec::new();
    for g in 0..count {
        let top = if g % 3 == 0 { 10 } else if g % 3 == 1 { 100 } else { 1000 };
        let answers: Vec<i64> = (0..1000).map(|_| next_random(&mut seed) % top).collect();
        forests.push(answers);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..50000i64 {
        let g = (round * 7) % count;
        let rabbits = num_rabbits(&forests[g as usize]);
        total += rabbits;
        checksum = (checksum * 31 + rabbits + g) % 1000000007;
    }
    println!("50000 rounds of 1000 answers: {total} rabbits, checksum {checksum}");
}
