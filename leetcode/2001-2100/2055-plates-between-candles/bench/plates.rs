// LeetCode #2055: Plates Between Candles -- Rust mirror of the ★ arm's
// benchmark (plates.kara): the same 50 strings and five million queries,
// the string collected into `Vec<char>` as the Kāra arm does, the same
// plate counts and nearest candles.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn plates_between_candles(s: &str, queries: &[(i64, i64)]) -> Vec<i64> {
    let places: Vec<char> = s.chars().collect();
    let n = places.len();
    let mut plates = vec![0i64; n + 1];
    let mut candle_before = vec![-1i64; n];
    let mut last = -1i64;
    for i in 0..n {
        plates[i + 1] = plates[i] + if places[i] == '*' { 1 } else { 0 };
        if places[i] == '|' {
            last = i as i64;
        }
        candle_before[i] = last;
    }
    let mut candle_after = vec![n as i64; n];
    let mut next = n as i64;
    for i in (0..n).rev() {
        if places[i] == '|' {
            next = i as i64;
        }
        candle_after[i] = next;
    }
    let mut answers = Vec::new();
    for &(left, right) in queries {
        let first = candle_after[left as usize];
        let last = candle_before[right as usize];
        answers.push(if first < last { plates[last as usize] - plates[first as usize] } else { 0 });
    }
    answers
}

fn main() {
    let mut seed = 2055;
    let mut total = 0i64;
    let mut check = 0i64;
    for t in 0..50 {
        let every = t + 1;
        let mut s = String::new();
        for _ in 0..100000 {
            s.push(if next_random(&mut seed) % every == 0 { '|' } else { '*' });
        }
        let mut queries = Vec::new();
        for _ in 0..100000 {
            let a = wide(&mut seed) % 100000;
            let b = wide(&mut seed) % 100000;
            queries.push((a.min(b), a.max(b)));
        }
        for a in plates_between_candles(&s, &queries) {
            total += a;
            check = (check * 31 + a + 1) % 1000000007;
        }
    }
    println!("50 strings: sum {total}, checksum {check}");
}
