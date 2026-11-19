// LeetCode #1643: Kth Smallest Instructions -- the bench's Rust mirror:
// the ★ arm on 1000000 random destinations of 1 to 15 rows and columns,
// each with a k drawn from all of its paths, all drawn first.

fn kth_smallest_path(destination: &[i32], k: i32) -> String {
    let (mut v, mut h) = (destination[0] as usize, destination[1] as usize);
    let n = v + h;
    let mut choose = vec![vec![0i64; n + 1]; n + 1];
    for i in 0..=n {
        choose[i][0] = 1;
        for j in 1..=i {
            choose[i][j] = choose[i - 1][j - 1] + choose[i - 1][j];
        }
    }
    let mut k = k as i64;
    let mut path = String::new();
    for _ in 0..n {
        let starting_h = choose[h + v - 1][v];
        if k <= starting_h {
            path.push('H');
            h -= 1;
        } else {
            path.push('V');
            k -= starting_h;
            v -= 1;
        }
    }
    path
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn count_paths(row: i64, column: i64) -> i64 {
    let mut count = 1;
    for i in 1..=row {
        count = count * (column + i) / i;
    }
    count
}

fn main() {
    let cases = 1000000;
    let mut seed: i64 = 1643;
    let mut drawn = Vec::new();
    for _ in 0..cases {
        let row = next_random(&mut seed) % 15 + 1;
        let column = next_random(&mut seed) % 15 + 1;
        let k = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % count_paths(row, column) + 1;
        drawn.push((row as i32, column as i32, k as i32));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for &(row, column, k) in &drawn {
        let path = kth_smallest_path(&[row, column], k);
        total += path.find('V').unwrap() as i64;
        for b in path.bytes() {
            check = (check * 3 + if b == b'H' { 1 } else { 2 }) % 1000000007;
        }
    }
    println!("{} destinations of up to 15 by 15: first moves down sum to {}, checksum {}", cases, total, check);
}
