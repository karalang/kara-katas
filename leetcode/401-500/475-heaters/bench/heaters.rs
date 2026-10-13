// Benchmark for #475: Rust mirror of the ★ arm (sort the heaters, binary
// search per house); see heaters.kara.

fn first_at_or_after(heaters: &[i64], x: i64) -> usize {
    let mut lo = 0;
    let mut hi = heaters.len();
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if heaters[mid] < x {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo
}

fn find_radius(houses: &[i64], heaters: &[i64]) -> i64 {
    let mut sorted = heaters.to_vec();
    sorted.sort();
    let mut radius = 0;
    for &house in houses {
        let at = first_at_or_after(&sorted, house);
        let mut nearest = i64::MAX;
        if at < sorted.len() {
            nearest = sorted[at] - house;
        }
        if at > 0 && house - sorted[at - 1] < nearest {
            nearest = house - sorted[at - 1];
        }
        if nearest > radius {
            radius = nearest;
        }
    }
    radius
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 475;
    let mut houses: Vec<i64> = Vec::new();
    for _ in 0..30000 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        houses.push(1 + (a * 32768 + b) % 1000000000);
    }
    let rounds = 200;
    let mut total = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let mut heaters: Vec<i64> = Vec::new();
        for _ in 0..30000 {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            heaters.push(1 + (a * 32768 + b) % 1000000000);
        }
        let got = find_radius(&houses, &heaters);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    println!("{} rounds of 30000 houses and 30000 heaters: radii add up to {}, checksum {}", rounds, total, checksum);
}
