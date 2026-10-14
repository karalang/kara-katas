// Benchmark for #546: Rust mirror of the ★ arm (memoized, with the
// boxes carried along); see remove_boxes.kara.

fn best(boxes: &[i64], l: i64, r: i64, k: i64, memo: &mut Vec<i64>) -> i64 {
    if l > r {
        return 0;
    }
    let n = boxes.len() as i64;
    let key = ((l * n + r) * n + k) as usize;
    if memo[key] >= 0 {
        return memo[key];
    }
    let mut i = l;
    let mut run = k + 1;
    while i < r && boxes[(i + 1) as usize] == boxes[l as usize] {
        i += 1;
        run += 1;
    }
    let mut most = run * run + best(boxes, i + 1, r, 0, memo);
    for m in i + 2..r + 1 {
        if boxes[m as usize] == boxes[l as usize] && boxes[(m - 1) as usize] != boxes[l as usize] {
            most = most.max(best(boxes, i + 1, m - 1, 0, memo) + best(boxes, m, r, run, memo));
        }
    }
    memo[key] = most;
    most
}

fn remove_boxes(boxes: &[i64]) -> i64 {
    let n = boxes.len();
    let mut memo = vec![-1; n * n * n];
    best(boxes, 0, n as i64 - 1, 0, &mut memo)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 40 random rows of 100 boxes (the problem's most), from 2 to 9
    // colours by the row, built once. Then 5 times over every row is
    // answered and the points go into the checksum.
    let rows = 40;
    let mut seed: i64 = 546;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for g in 0..rows {
        let colours = 2 + g % 8;
        all.push((0..100).map(|_| 1 + next_random(&mut seed) % colours).collect());
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for _ in 0..5 {
        for t in 0..rows as usize {
            let points = remove_boxes(&all[t]);
            total += points;
            checksum = (checksum * 31 + points) % 1000000007;
        }
    }
    println!("{rows} rows, 5 times each: {total} points, checksum {checksum}");
}
