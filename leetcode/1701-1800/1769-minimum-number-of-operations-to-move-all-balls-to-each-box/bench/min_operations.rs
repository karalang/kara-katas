// LeetCode #1769: Minimum Number of Operations to Move All Balls to Each
// Box -- the bench in Rust, mirroring min_operations.kara: two sweeps over
// the row's bytes.
fn min_operations(boxes: &str) -> Vec<i32> {
    let b = boxes.as_bytes();
    let n = b.len();
    let mut answer = vec![0i32; n];
    let (mut balls, mut moves) = (0i32, 0i32);
    for i in 0..n {
        answer[i] += moves;
        if b[i] == b'1' {
            balls += 1;
        }
        moves += balls;
    }
    balls = 0;
    moves = 0;
    for i in (0..n).rev() {
        answer[i] += moves;
        if b[i] == b'1' {
            balls += 1;
        }
        moves += balls;
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1769;
    let mut rows: Vec<String> = Vec::new();
    for _ in 0..200 {
        let full = next_random(&mut seed) % 101;
        let s: String = (0..2000).map(|_| if next_random(&mut seed) % 100 < full { '1' } else { '0' }).collect();
        rows.push(s);
    }
    let mut check: i64 = 0;
    for call in 0..40000i64 {
        let answer = min_operations(&rows[((check + call * 7919) % 200) as usize]);
        check = (check * 31 + answer[(check % 2000) as usize] as i64) % 1000000007;
    }
    println!("40000 calls over 200 rows: checksum {}", check);
}
