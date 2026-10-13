// Benchmark for #479: Rust mirror of the ★ arm (palindromes from the
// top); see largest_palindrome_product.kara.

fn largest_palindrome(n: i64) -> i64 {
    if n == 1 {
        return 9;
    }
    let mut upper: i64 = 1;
    for _ in 0..n {
        upper *= 10;
    }
    let lower = upper / 10;
    upper -= 1;
    let mut half = upper;
    while half >= lower {
        let mut palindrome = half;
        let mut rest = half;
        while rest > 0 {
            palindrome = palindrome * 10 + rest % 10;
            rest /= 10;
        }
        let mut factor = upper;
        while factor * factor >= palindrome {
            if palindrome % factor == 0 && palindrome / factor >= lower {
                return palindrome % 1337;
            }
            factor -= 1;
        }
        half -= 1;
    }
    -1
}

fn main() {
    let rounds = 10;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for n in 1..9 {
            let got = largest_palindrome(n);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    println!("{} rounds of n = 1 to 8: answers add up to {}, checksum {}", rounds, total, checksum);
}
