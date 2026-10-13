// Benchmark for #526: Rust mirror of the ★ arm (place positions from the
// front); see count_arrangement.kara.

fn place(n: i64, pos: i64, used: &mut Vec<bool>) -> i64 {
    if pos > n {
        return 1;
    }
    let mut count = 0;
    for x in 1..=n {
        if !used[x as usize] && (x % pos == 0 || pos % x == 0) {
            used[x as usize] = true;
            count += place(n, pos + 1, used);
            used[x as usize] = false;
        }
    }
    count
}

fn count_arrangement(n: i64) -> i64 {
    let mut used = vec![false; (n + 1) as usize];
    place(n, 1, &mut used)
}

fn main() {
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..20 {
        for n in 1..=15 {
            let count = count_arrangement(n);
            total += count;
            checksum = (checksum * 31 + count + round) % 1000000007;
        }
    }
    println!("n from 1 to 15, 20 rounds: total {}, checksum {}", total, checksum);
}
