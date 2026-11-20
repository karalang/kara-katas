// LeetCode #2355: Maximum Number of Books You Can Take -- the bench, the ★
// arm in Rust: the most books from a run ending at each shelf, from the
// nearest shelf to the left that caps the run, found on a monotonic stack.

fn maximum_books(books: &[i64]) -> i64 {
    let n = books.len();
    let mut best = vec![0i64; n];
    let mut stack: Vec<usize> = Vec::new();
    let mut answer = 0i64;
    for i in 0..n {
        while let Some(&top) = stack.last() {
            if books[top] - top as i64 >= books[i] - i as i64 {
                stack.pop();
            } else {
                break;
            }
        }
        best[i] = match stack.last() {
            Some(&j) => {
                let length = (i - j) as i64;
                length * books[i] - length * (length - 1) / 2 + best[j]
            }
            None => {
                let length = ((i + 1) as i64).min(books[i]);
                length * books[i] - length * (length - 1) / 2
            }
        };
        stack.push(i);
        answer = answer.max(best[i]);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // array a holds 10^5 shelves: up to 10^5 books every (a + 2)^2-th
    // shelf, up to 100 (a + 1) between
    let mut seed = 2355i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..10i64 {
        let mut books = Vec::new();
        for i in 0..100000i64 {
            let r = next_random(&mut seed);
            books.push(if i % ((a + 2) * (a + 2)) == 0 { r * 3 % 100001 } else { r % (100 * (a + 1) + 1) });
        }
        arrays.push(books);
    }
    let mut check = 0i64;
    for p in 0..50i64 {
        for books in &arrays {
            check = (check * 31 + maximum_books(books) % 1000000007 + p) % 1000000007;
        }
    }
    println!("50 passes over 10 arrays of 10^5 shelves: checksum {}", check);
}
