// Benchmark for #670: the last place of each digit, as the Kara ★ arm.

fn digits_of(num: i64) -> Vec<i64> {
    let mut d: Vec<i64> = Vec::new();
    let mut x = num;
    while x > 0 {
        d.push(x % 10);
        x /= 10;
    }
    if d.is_empty() {
        d.push(0);
    }
    d.reverse();
    d
}

fn number_of(d: &[i64]) -> i64 {
    d.iter().fold(0, |x, &v| x * 10 + v)
}

fn maximum_swap(num: i64) -> i64 {
    let mut d = digits_of(num);
    let mut last = vec![-1i64; 10];
    for i in 0..d.len() {
        last[d[i] as usize] = i as i64;
    }
    for i in 0..d.len() {
        let mut v = 9;
        while v > d[i] {
            if last[v as usize] > i as i64 {
                let j = last[v as usize] as usize;
                d[j] = d[i];
                d[i] = v;
                return number_of(&d);
            }
            v -= 1;
        }
    }
    num
}

fn main() {
    let count: i64 = 3000000;
    let mut sum: i64 = 0;
    for i in 0..count {
        sum = (sum * 31 + maximum_swap(i * 33 + i % 7)) % 1000000007;
    }
    println!("{} numbers: checksum {}", count, sum);
}
