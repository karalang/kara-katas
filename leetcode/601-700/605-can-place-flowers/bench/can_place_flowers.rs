// Benchmark for #605: Rust mirror of the ★ arm (plant greedily); see
// can_place_flowers.kara. The bed is copied into a fresh `Vec` on every
// call, as the Kāra arm clones it.

fn can_place_flowers(flowerbed: &[i64], n: i64) -> bool {
    let mut bed = flowerbed.to_vec();
    let mut planted = 0;
    for i in 0..bed.len() {
        if bed[i] == 0 && (i == 0 || bed[i - 1] == 0) && (i == bed.len() - 1 || bed[i + 1] == 0) {
            bed[i] = 1;
            planted += 1;
        }
    }
    planted >= n
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let rounds = 50;
    let size = 20000;
    let mut seed: i64 = 605;
    let mut beds: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let spread = 2 + step(&mut seed) % 5;
        let mut bed: Vec<i64> = Vec::new();
        for i in 0..size {
            if step(&mut seed) % spread == 0 && (i == 0 || bed[i - 1] == 0) {
                bed.push(1);
            } else {
                bed.push(0);
            }
        }
        beds.push(bed);
    }
    let mut yes = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds as i64 {
        for g in 0..count as i64 {
            let n = (round * 397 + g * 113) % 8000;
            let fits = can_place_flowers(&beds[((round * 7 + g) % count as i64) as usize], n);
            if fits {
                yes += 1;
            }
            checksum = (checksum * 31 + n * 2 + if fits { 1 } else { 0 }) % 1000000007;
        }
    }
    println!("{} beds, {} rounds: {} fit, checksum {}", count, rounds, yes, checksum);
}
