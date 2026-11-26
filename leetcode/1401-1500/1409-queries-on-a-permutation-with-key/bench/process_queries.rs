// LeetCode #1409 bench, Rust: the same P, each query found and the part up
// to it turned one place, workload and checksum as process_queries.kara.

fn process_queries(queries: &Vec<i32>, m: i32) -> Vec<i32> {
    let mut p: Vec<i32> = (1..=m).collect();
    let mut answer = Vec::new();
    for &q in queries.iter() {
        let at = p.iter().position(|&x| x == q).unwrap();
        answer.push(at as i32);
        p[..=at].rotate_right(1);
    }
    answer
}

fn main() {
    let mut seed: i64 = 1409;
    let mut check: i64 = 0;
    for _ in 0..300 {
        let mut queries: Vec<i32> = Vec::new();
        for _ in 0..1000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            queries.push((1 + seed / 65536 % 1000) as i32);
        }
        for &x in process_queries(&queries, 1000).iter() {
            check = (check * 131 + x as i64) % 1000000007;
        }
    }
    println!("300 rounds of 10^3 queries: checksum {}", check);
}
