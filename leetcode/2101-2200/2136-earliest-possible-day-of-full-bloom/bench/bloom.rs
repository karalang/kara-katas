// LeetCode #2136: Earliest Possible Day of Full Bloom -- the benchmark,
// the same algorithm as bloom.kara.

fn earliest_full_bloom(plant_time: &[i64], grow_time: &[i64]) -> i64 {
    let mut order: Vec<usize> = (0..plant_time.len()).collect();
    order.sort_by(|&a, &b| grow_time[b].cmp(&grow_time[a]));
    let mut planted = 0;
    let mut bloom = 0;
    for &i in order.iter() {
        planted += plant_time[i];
        bloom = bloom.max(planted + grow_time[i]);
    }
    bloom
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2136;
    let mut plants: Vec<Vec<i64>> = Vec::new();
    let mut grows: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut plant = Vec::new();
        let mut grow = Vec::new();
        for _ in 0..100000 {
            plant.push(next_random(&mut seed) % 10000 + 1);
            grow.push(next_random(&mut seed) % 10000 + 1);
        }
        plants.push(plant);
        grows.push(grow);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..10 {
        for g in 0..10 {
            let hi = next_random(&mut seed);
            let at = ((hi * 32768 + next_random(&mut seed)) % 100000) as usize;
            plants[g][at] = next_random(&mut seed) % 10000 + 1;
            grows[g][at] = next_random(&mut seed) % 10000 + 1;
            let day = earliest_full_bloom(&plants[g], &grows[g]);
            total += day;
            check = (check * 31 + day + round) % 1000000007;
        }
    }
    println!("100 solves: {} days in all, checksum {}", total, check);
}
