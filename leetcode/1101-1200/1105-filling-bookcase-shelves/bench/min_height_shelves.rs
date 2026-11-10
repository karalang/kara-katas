// LeetCode #1105: Filling Bookcase Shelves -- the bench in Rust: the ★
// arm (the least height for the first i books over every run ending at
// book i that fits a shelf) over 32 bookcases of 1000 books, each round
// changing one book in every bookcase and solving it again.

fn min_height_shelves(books: &Vec<Vec<i64>>, shelf_width: i64) -> i64 {
    let n = books.len();
    let mut best: Vec<i64> = vec![0; n + 1];
    for i in 1..n + 1 {
        let mut width = 0;
        let mut tallest = 0;
        best[i] = i64::MAX;
        let mut j = i;
        while j > 0 && width + books[j - 1][0] <= shelf_width {
            width += books[j - 1][0];
            tallest = tallest.max(books[j - 1][1]);
            best[i] = best[i].min(best[j - 1] + tallest);
            j -= 1;
        }
    }
    best[n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1105i64;
    let mut cases: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..32 {
        let books: Vec<Vec<i64>> = (0..1000)
            .map(|_| {
                let t = next_random(&mut seed) % 50 + 1;
                vec![t, next_random(&mut seed) % 1000 + 1]
            })
            .collect();
        cases.push(books);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..200i64 {
        for j in 0..cases.len() {
            let at = ((round * 7919 + j as i64 * 104729) % 1000) as usize;
            cases[j][at][0] = (cases[j][at][0] * 7 + round) % 50 + 1;
            cases[j][at][1] = (cases[j][at][1] * 13 + j as i64) % 1000 + 1;
            let h = min_height_shelves(&cases[j], 1000);
            total += h;
            check = (check * 31 + h) % 1000000007;
        }
    }
    println!("200 rounds over 32 bookcases of 1000 books: heights total {}, checksum {}", total, check);
}
