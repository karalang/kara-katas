// Benchmark for #506 in Rust: the ★ arm (the athletes sorted by score);
// see ../find_relative_ranks.kara. A stable sort_by_key on the negated
// score, and a fresh String for every rank.

fn find_relative_ranks(score: &[i64]) -> Vec<String> {
    let n = score.len();
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by_key(|&i| -score[i]);
    let mut answer = vec![String::new(); n];
    for place in 0..n {
        answer[order[place]] = match place {
            0 => "Gold Medal".to_string(),
            1 => "Silver Medal".to_string(),
            2 => "Bronze Medal".to_string(),
            _ => format!("{}", place + 1),
        };
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 500 lists of 10,000 athletes (the problem's most), all different
    // scores from 0 to 10^6 (the j-th is j * 100 plus less than 100,
    // shuffled), built once. Then each list is ranked once, the length
    // of every rank folded into a checksum.
    let lists = 500;
    let n: i64 = 10000;
    let mut seed: i64 = 506;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..lists {
        let mut score: Vec<i64> = Vec::new();
        for j in 0..n {
            score.push(j * 100 + next_random(&mut seed) % 100);
        }
        let mut k = n - 1;
        while k > 0 {
            let other = next_random(&mut seed) % (k + 1);
            score.swap(k as usize, other as usize);
            k -= 1;
        }
        all.push(score);
    }
    let mut letters: i64 = 0;
    let mut checksum: i64 = 0;
    for c in 0..lists {
        for rank in find_relative_ranks(&all[c]) {
            letters += rank.len() as i64;
            checksum = (checksum * 31 + rank.len() as i64) % 1000000007;
        }
    }
    println!("{lists} lists of {n} athletes: {letters} characters, checksum {checksum}");
}
