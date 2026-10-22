// Benchmark for #853: Car Fleet -- Rust twin of the Kāra ★ arm (closest to
// the target first).

fn car_fleet(target: i64, position: &[i64], speed: &[i64]) -> i64 {
    let mut cars: Vec<(i64, i64)> = Vec::new();
    for i in 0..position.len() {
        cars.push((position[i], speed[i]));
    }
    cars.sort();
    let mut fleets = 0;
    let mut far: i64 = 0;
    let mut fast: i64 = 1;
    for &(p, s) in cars.iter().rev() {
        if (target - p) * fast > far * s {
            fleets += 1;
            far = target - p;
            fast = s;
        }
    }
    fleets
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: usize = 64;
    let rounds = 150;
    let n = 100000;
    let target: i64 = 1000000;
    let mut seed: i64 = 853;
    let mut positions: Vec<Vec<i64>> = Vec::new();
    let mut speeds: Vec<Vec<i64>> = Vec::new();
    for g in 0..count {
        let top = 1 + (g % 8) as i64 * 142857;
        let mut taken: Vec<bool> = vec![false; target as usize];
        let mut position: Vec<i64> = Vec::new();
        while position.len() < n {
            let p = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % target;
            if !taken[p as usize] {
                taken[p as usize] = true;
                position.push(p);
            }
        }
        let mut speed: Vec<i64> = Vec::new();
        for _ in 0..n {
            speed.push(1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % top);
        }
        positions.push(position);
        speeds.push(speed);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = round % count;
        let f = car_fleet(target, &positions[g], &speeds[g]);
        total += f;
        checksum = (checksum * 31 + f) % 1000000007;
    }
    println!("{} rounds of {} roads: fleets sum to {}, checksum {}", rounds, count, total, checksum);
}
