// LeetCode #2226: Maximum Candies Allocated to K Children -- the
// benchmark's Rust mirror of candies.kara: a binary search on the
// answer, x candies each possible when the piles give k shares of x.

fn maximum_candies(candies: &[i64], k: i64) -> i64 {
    let mut low = 0;
    let mut high = *candies.iter().max().unwrap_or(&0);
    while low < high {
        let x = (low + high + 1) / 2;
        let mut shares = 0;
        for &pile in candies {
            shares += pile / x;
        }
        if shares >= k {
            low = x;
        } else {
            high = x - 1;
        }
    }
    low
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2226;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..4 {
        lists.push((0..100000).map(|_| wide_random(&mut seed) % 10000000 + 1).collect());
    }
    let children = [1000i64, 1000000, 1000000000, 100000000000];
    let mut check: i64 = 0;
    for _ in 0..25 {
        for l in 0..4 {
            // punch: one pile is drawn again before each answer
            let at = (wide_random(&mut seed) % 100000) as usize;
            lists[l][at] = wide_random(&mut seed) % 10000000 + 1;
            check = (check * 31 + maximum_candies(&lists[l], children[l])) % 1000000007;
        }
    }
    println!("100 answers over 10^5 piles: checksum {check}");
}
