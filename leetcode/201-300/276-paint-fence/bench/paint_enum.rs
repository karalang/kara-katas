// LeetCode 276 bench mirror — brute-force enumeration, Rust.
// Same algorithm as paint_enum.kara; sequential over the 16 prefixes.

const N: usize = 13;
const K: i64 = 4;

fn count_prefix(p0: i64, p1: i64) -> i64 {
    let mut c = [0i64; N];
    c[0] = p0;
    c[1] = p1;
    let mut count = 0i64;
    loop {
        let mut ok = true;
        for i in 2..N {
            if c[i] == c[i - 1] && c[i - 1] == c[i - 2] {
                ok = false;
            }
        }
        if ok {
            count += 1;
        }
        let mut p = N as i64 - 1;
        while p >= 2 && c[p as usize] == K - 1 {
            c[p as usize] = 0;
            p -= 1;
        }
        if p < 2 {
            break;
        }
        c[p as usize] += 1;
    }
    count
}

fn main() {
    let mut total = 0i64;
    for pre in 0..K * K {
        total += count_prefix(pre / K, pre % K);
    }
    println!("{}", total);
}
