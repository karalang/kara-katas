// LeetCode #1215: Stepping Numbers -- the bench in Rust: the ★ arm (a
// breadth-first search from the digits 1 to 9, stopping at the first
// number past `high`) on the same 2000 ranges and 20 rounds.

fn count_stepping_numbers(low: i64, high: i64) -> Vec<i64> {
    let mut out = Vec::new();
    if low == 0 {
        out.push(0);
    }
    let mut queue: Vec<i64> = (1..10).collect();
    let mut head = 0;
    while head < queue.len() {
        let n = queue[head];
        head += 1;
        if n > high {
            break;
        }
        if n >= low {
            out.push(n);
        }
        let last = n % 10;
        if last > 0 {
            queue.push(n * 10 + last - 1);
        }
        if last < 9 {
            queue.push(n * 10 + last + 1);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1215;
    let mut ranges = Vec::new();
    for _ in 0..2000 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let low = (a * 32768 + b) % 2000000001;
        let c = next_random(&mut seed);
        let d = next_random(&mut seed);
        let high = low + (c * 32768 + d) % (2000000001 - low);
        ranges.push((low, high));
    }
    let mut check: i64 = 0;
    for round in 0..20 {
        for &(low, high) in ranges.iter() {
            let answer = count_stepping_numbers(low, high);
            let last = if !answer.is_empty() { answer[answer.len() - 1] } else { -1 };
            check = (check * 131 + answer.len() as i64 + last % 1000003 + round) % 1000000007;
        }
    }
    println!("20 rounds over 2000 ranges: checksum {}", check);
}
