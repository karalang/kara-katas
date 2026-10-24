// Benchmark: LeetCode #948 Bag of Tokens -- the ★ arm, sorted and played
// from both ends, on bags of 1000 tokens, LeetCode's largest. Mirrors
// bag_of_tokens_score.kara, .c, .py and go-seq/.

fn bag_of_tokens_score(tokens: &[i64], power: i64) -> i64 {
    let mut t = tokens.to_vec();
    t.sort();
    let mut lo: i64 = 0;
    let mut hi = t.len() as i64 - 1;
    let mut p = power;
    let mut score = 0;
    let mut best = 0;
    while lo <= hi {
        if p >= t[lo as usize] {
            p -= t[lo as usize];
            lo += 1;
            score += 1;
            best = best.max(score);
        } else if score > 0 && lo < hi {
            p += t[hi as usize];
            hi -= 1;
            score -= 1;
        } else {
            break;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, n) = (500, 20, 1000);
    let mut seed = 948;
    let mut bags: Vec<Vec<i64>> = Vec::new();
    let mut powers: Vec<i64> = Vec::new();
    for _ in 0..count {
        let mut tokens: Vec<i64> = Vec::new();
        for _ in 0..n {
            tokens.push(next_random(&mut seed) % 10000);
        }
        bags.push(tokens);
        powers.push(next_random(&mut seed) % 10000);
    }
    let mut total = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let b = (r + i) % count;
            let s = bag_of_tokens_score(&bags[b], powers[b]);
            total += s;
            check = (check * 1000003 + s) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} bags of {n} tokens: scores adding to {total}, checksum {check}");
}
