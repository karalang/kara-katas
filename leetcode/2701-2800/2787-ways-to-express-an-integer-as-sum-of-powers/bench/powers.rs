// LeetCode #2787: Ways to Express an Integer as Sum of Powers -- the bench
// in Rust: the ★ arm over every n from 1 to 300 with every x from 1 to 5,
// 20 times over.

fn number_of_ways(n: i64, x: i64) -> i64 {
    let modulus = 1000000007;
    let mut ways = vec![0i64; (n + 1) as usize];
    ways[0] = 1;
    let mut i: i64 = 1;
    while i.pow(x as u32) <= n {
        let p = i.pow(x as u32);
        for s in (p..=n).rev() {
            ways[s as usize] = (ways[s as usize] + ways[(s - p) as usize]) % modulus;
        }
        i += 1;
    }
    ways[n as usize]
}

fn main() {
    let rounds = 20;
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for n in 1..=300 {
            for x in 1..=5 {
                let w = number_of_ways(n, x);
                total += w;
                check = (check * 31 + w + r) % 1000000007;
            }
        }
    }
    println!("1500 pairs, {rounds} rounds: ways sum to {total}, checksum {check}");
}
