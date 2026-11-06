// LeetCode #1057: Campus Bikes -- the benchmark, mirror of campus_bikes.kara.

fn assign_bikes(workers: &[(i64, i64)], bikes: &[(i64, i64)]) -> Vec<i64> {
    let mut buckets: Vec<Vec<(i64, i64)>> = vec![Vec::new(); 2000];
    for (w, &(wx, wy)) in workers.iter().enumerate() {
        for (b, &(bx, by)) in bikes.iter().enumerate() {
            let d = (wx - bx).abs() + (wy - by).abs();
            buckets[d as usize].push((w as i64, b as i64));
        }
    }
    let mut bike_of = vec![-1i64; workers.len()];
    let mut taken = vec![false; bikes.len()];
    let mut left = workers.len();
    for bucket in buckets.iter() {
        for &(w, b) in bucket.iter() {
            if left > 0 && bike_of[w as usize] < 0 && !taken[b as usize] {
                bike_of[w as usize] = b;
                taken[b as usize] = true;
                left -= 1;
            }
        }
    }
    bike_of
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_places(count: i64, seed: &mut i64) -> Vec<(i64, i64)> {
    let mut places = Vec::new();
    for _ in 0..count {
        let x = next_random(seed) % 1000;
        let y = next_random(seed) % 1000;
        places.push((x, y));
    }
    places
}

fn main() {
    let count = 20;
    let rounds = 8;
    let mut seed = 1057;
    let mut campuses: Vec<(Vec<(i64, i64)>, Vec<(i64, i64)>)> = Vec::new();
    for _ in 0..count {
        let workers = random_places(300, &mut seed);
        let bikes = random_places(400, &mut seed);
        campuses.push((workers, bikes));
    }
    let mut ridden: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for (workers, bikes) in campuses.iter() {
            let answer = assign_bikes(workers, bikes);
            for (w, &b) in answer.iter().enumerate() {
                let b = b as usize;
                ridden += (workers[w].0 - bikes[b].0).abs() + (workers[w].1 - bikes[b].1).abs();
                check = (check * 131 + b as i64 + 1) % 1000000007;
            }
        }
    }
    println!("{} campuses of 300 workers and 400 bikes, {} rounds: {} ridden, checksum {}", count, rounds, ridden, check);
}
