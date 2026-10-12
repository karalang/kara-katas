// Benchmark for #458: mirror of poor_pigs.kara (the ★ arm, growing the
// number of outcomes) on the same workload.

fn poor_pigs(buckets: i64, minutes_to_die: i64, minutes_to_test: i64) -> i64 {
    let states = minutes_to_test / minutes_to_die + 1;
    let mut pigs = 0;
    let mut covered = 1;
    while covered < buckets {
        covered *= states;
        pigs += 1;
    }
    pigs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 1000000;
    let rounds = 20;
    let mut seed: i64 = 458;
    let mut buckets: Vec<i64> = Vec::new();
    let mut die: Vec<i64> = Vec::new();
    let mut test: Vec<i64> = Vec::new();
    for _ in 0..n {
        let digits = next_random(&mut seed) % 13;
        let mut top: i64 = 1;
        for _ in 0..digits {
            top *= 10;
        }
        let r = (next_random(&mut seed) * 65536 + next_random(&mut seed)) * 65536 + next_random(&mut seed);
        buckets.push(1 + r % top);
        let d = 1 + next_random(&mut seed) % 100;
        die.push(d);
        test.push(d + next_random(&mut seed) % (101 - d));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let k = (next_random(&mut seed) * 65536 + next_random(&mut seed)) % n;
        buckets[k as usize] = 1 + (next_random(&mut seed) * 65536 + next_random(&mut seed)) % 1000000000000;
        let mut sum = 0;
        for i in 0..n as usize {
            sum += poor_pigs(buckets[i], die[i], test[i]);
        }
        total += sum;
        checksum = (checksum * 31 + sum) % 1000000007;
    }
    println!("{} rounds on {} queries: {} pigs, checksum {}", rounds, n, total, checksum);
}
