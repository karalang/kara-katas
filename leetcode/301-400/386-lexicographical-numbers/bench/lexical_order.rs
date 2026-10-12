// Benchmark for #386: mirror of lexical_order.kara (step to the next number).

fn lexical_order(n: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let mut cur = 1i64;
    for _ in 0..n {
        out.push(cur);
        if cur * 10 <= n {
            cur *= 10;
        } else {
            while cur % 10 == 9 || cur + 1 > n {
                cur /= 10;
            }
            cur += 1;
        }
    }
    out
}

fn main() {
    let mut checksum: i64 = 0;
    for q in 0..6000i64 {
        let v = lexical_order(50000 - q % 1000);
        let mut sum: i64 = 0;
        for k in 0..v.len() {
            sum += v[k] * (k as i64 + 1);
        }
        checksum = (checksum * 31 + sum) % 1000000007;
    }
    println!("6000 lists, checksum {}", checksum);
}
