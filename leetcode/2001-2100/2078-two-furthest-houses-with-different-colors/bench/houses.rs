// LeetCode #2078: Two Furthest Houses With Different Colors -- Rust mirror
// of the ★ arm's benchmark (houses.kara): 20000 streets of 100 houses,
// 1000 rounds each recoloring one house of every street and answering
// every street that still has two colors with a scan in from each end.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn max_distance(colors: &[i64]) -> i64 {
    let n = colors.len();
    let mut j = n - 1;
    while colors[j] == colors[0] {
        j -= 1;
    }
    let mut i = 0;
    while colors[i] == colors[n - 1] {
        i += 1;
    }
    j.max(n - 1 - i) as i64
}

fn main() {
    let mut seed = 2078;
    let mut streets: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20000 {
        let mut colors = vec![0i64; 100];
        let a = next_random(&mut seed) % 100;
        colors[a as usize] = next_random(&mut seed) % 3 + 1;
        let b = next_random(&mut seed) % 100;
        colors[b as usize] = next_random(&mut seed) % 3 + 1;
        streets.push(colors);
    }
    let (mut answered, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..1000 {
        for colors in streets.iter_mut() {
            let k = next_random(&mut seed) % 100;
            colors[k as usize] = if next_random(&mut seed) % 2 == 0 { 0 } else { next_random(&mut seed) % 3 + 1 };
            if colors.iter().any(|&c| c != colors[0]) {
                let a = max_distance(colors);
                answered += 1;
                total += a;
                check = (check * 31 + a) % 1000000007;
            }
        }
    }
    println!("{} answers: sum {}, checksum {}", answered, total, check);
}
