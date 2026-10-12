// Benchmark for #455: mirror of assign_cookies.kara (the ★ arm, both
// sorted, least greedy child first) on the same workload.

fn find_content_children(g: &[i64], s: &[i64]) -> i64 {
    let mut greed = g.to_vec();
    greed.sort();
    let mut sizes = s.to_vec();
    sizes.sort();
    let mut child = 0;
    for &size in &sizes {
        if child < greed.len() && size >= greed[child] {
            child += 1;
        }
    }
    child as i64
}

// ---- benchmark --------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    1 + (hi * 65536 + lo) % 1000000000
}

fn main() {
    let n: i64 = 1000000;
    let rounds = 10;
    let mut seed: i64 = 455;
    let mut g: Vec<i64> = Vec::new();
    let mut s: Vec<i64> = Vec::new();
    for _ in 0..n {
        g.push(random_value(&mut seed));
        s.push(random_value(&mut seed));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let hi = next_random(&mut seed);
        let lo = next_random(&mut seed);
        let at = ((hi * 65536 + lo) % n) as usize;
        g[at] = random_value(&mut seed);
        let hi = next_random(&mut seed);
        let lo = next_random(&mut seed);
        let at = ((hi * 65536 + lo) % n) as usize;
        s[at] = random_value(&mut seed);
        let fed = find_content_children(&g, &s);
        total += fed;
        checksum = (checksum * 31 + fed) % 1000000007;
    }
    println!(
        "{rounds} rounds on {n} children and {n} cookies: {total} content, checksum {checksum}"
    );
}
