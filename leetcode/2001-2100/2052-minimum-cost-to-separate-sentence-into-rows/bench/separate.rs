// LeetCode #2052: Minimum Cost to Separate Sentence Into Rows -- Rust
// mirror of the ★ arm's benchmark (separate.kara): the same 600 sentences,
// the same dynamic programming from the end.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn minimum_cost(sentence: &str, k: i64) -> i64 {
    let lens: Vec<i64> = sentence.split(' ').map(|w| w.len() as i64).collect();
    let n = lens.len();
    let mut best = vec![0i64; n + 1];
    for i in (0..n).rev() {
        let mut width = -1;
        let mut least = i64::MAX;
        let mut j = i;
        while j < n && width + 1 + lens[j] <= k {
            width += 1 + lens[j];
            j += 1;
            if j == n {
                least = 0;
            } else {
                least = least.min((k - width) * (k - width) + best[j]);
            }
        }
        best[i] = least;
    }
    best[0]
}

fn main() {
    let letters = b"abcdefghijklmnopqrstuvwxyz";
    let mut seed = 2052i64;
    let (mut sum, mut check) = (0i64, 0i64);
    for t in 0..600i64 {
        let mut text = String::new();
        while text.len() < 4990 {
            if !text.is_empty() {
                text.push(' ');
            }
            let len = next_random(&mut seed) % 10 + 1;
            for _ in 0..len {
                let at = (next_random(&mut seed) % 26) as usize;
                text.push(letters[at] as char);
            }
        }
        let k = 20 + t % 200 * 20;
        let cost = minimum_cost(&text, k);
        sum += cost;
        check = (check * 31 + cost) % 1000000007;
    }
    println!("600 sentences: sum {}, checksum {}", sum, check);
}
