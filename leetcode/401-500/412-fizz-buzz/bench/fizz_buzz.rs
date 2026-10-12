// Benchmark for #412: mirror of fizz_buzz.kara (test each case).

fn fizz_buzz(n: i64) -> Vec<String> {
    let mut answer: Vec<String> = Vec::new();
    for i in 1..n + 1 {
        if i % 15 == 0 {
            answer.push(String::from("FizzBuzz"));
        } else if i % 3 == 0 {
            answer.push(String::from("Fizz"));
        } else if i % 5 == 0 {
            answer.push(String::from("Buzz"));
        } else {
            answer.push(i.to_string());
        }
    }
    answer
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let calls: i64 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(2000);
    let mut seed: i64 = 412;
    let mut bytes: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..calls {
        let n = 9000 + step(&mut seed) % 1001;
        let answer = fizz_buzz(n);
        let mut length = 0;
        for s in &answer {
            length += s.len() as i64;
        }
        bytes += length;
        checksum = (checksum * 31 + length) % 1000000007;
    }
    println!("{} calls: {} bytes, checksum {}", calls, bytes, checksum);
}
