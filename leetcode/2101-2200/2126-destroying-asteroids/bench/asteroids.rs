// LeetCode #2126: Destroying Asteroids -- the benchmark, the same
// algorithm as asteroids.kara.

fn asteroids_destroyed(mass: i64, asteroids: &[i64]) -> bool {
    let mut sorted = asteroids.to_vec();
    sorted.sort();
    let mut planet = mass;
    for &a in sorted.iter() {
        if planet < a {
            return false;
        }
        planet += a;
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2126;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut asteroids: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            asteroids.push((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 99001 + 1000);
        }
        arrays.push(asteroids);
    }
    let mut destroyed = 0;
    let mut check: i64 = 0;
    for round in 0..10i64 {
        for k in 0..20usize {
            let at = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000) as usize;
            arrays[k][at] = next_random(&mut seed) % 2000 + 1;
            let mass = next_random(&mut seed) % 1000 + 500;
            if asteroids_destroyed(mass, &arrays[k]) {
                destroyed += 1;
                check = (check * 31 + round * 20 + k as i64) % 1000000007;
            }
        }
    }
    println!("200 solves: {} destroyed, checksum {}", destroyed, check);
}
