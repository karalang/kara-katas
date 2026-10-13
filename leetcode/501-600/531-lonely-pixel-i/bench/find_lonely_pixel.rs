// Benchmark for #531: Rust mirror of the ★ arm (count each row and
// column); see find_lonely_pixel.kara.

fn find_lonely_pixel(picture: &Vec<Vec<char>>) -> i64 {
    let (m, n) = (picture.len(), picture[0].len());
    let mut rows = vec![0i64; m];
    let mut cols = vec![0i64; n];
    for r in 0..m {
        for c in 0..n {
            if picture[r][c] == 'B' {
                rows[r] += 1;
                cols[c] += 1;
            }
        }
    }
    let mut lonely = 0;
    for r in 0..m {
        for c in 0..n {
            if picture[r][c] == 'B' && rows[r] == 1 && cols[c] == 1 {
                lonely += 1;
            }
        }
    }
    lonely
}

fn main() {
    // 20 pictures of 500 by 500 made once, black with a chance of 1 to 20
    // in 1,000; then every picture is answered 200 times.
    let mut seed: i64 = 531;
    let mut pictures: Vec<Vec<Vec<char>>> = Vec::new();
    for p in 0..20 {
        let per_mille = 1 + p;
        let mut picture: Vec<Vec<char>> = Vec::new();
        for _ in 0..500 {
            let mut row: Vec<char> = Vec::new();
            for _ in 0..500 {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                row.push(if seed / 65536 % 1000 < per_mille { 'B' } else { 'W' });
            }
            picture.push(row);
        }
        pictures.push(picture);
    }
    let mut total = 0i64;
    let mut checksum = 0i64;
    for _ in 0..200 {
        for p in 0..pictures.len() {
            let answer = find_lonely_pixel(&pictures[p]);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    println!("20 pictures of 500 by 500, 200 times each: total {}, checksum {}", total, checksum);
}
