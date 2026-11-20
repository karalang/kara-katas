// LeetCode #2326: Spiral Matrix IV -- the bench, the ★ arm in Rust. A
// walker starts at the top left heading right and writes the list's
// values one by one, turning clockwise when the next cell is off the grid
// or already written. O(m n). The list is walked by reference, as the
// others walk theirs without taking it apart.

struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

fn spiral_matrix(m: i64, n: i64, head: &Option<Box<ListNode>>) -> Vec<Vec<i64>> {
    let mut grid = vec![vec![-1i64; n as usize]; m as usize];
    let moves = [(0i64, 1i64), (1, 0), (0, -1), (-1, 0)];
    let (mut r, mut c, mut d) = (0i64, 0i64, 0usize);
    let mut node = head;
    while let Some(here) = node {
        grid[r as usize][c as usize] = here.val;
        let (nr, nc) = (r + moves[d].0, c + moves[d].1);
        if nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr as usize][nc as usize] != -1 {
            d = (d + 1) % 4;
        }
        r += moves[d].0;
        c += moves[d].1;
        node = &here.next;
    }
    grid
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn drop_list(mut head: Option<Box<ListNode>>) {
    while let Some(mut node) = head {
        head = node.next.take();
    }
}

fn main() {
    let rows = [100i64, 200, 250, 400, 500, 1000, 50, 125, 80, 160];
    let mut seed: i64 = 2326;
    let mut heads: Vec<Option<Box<ListNode>>> = Vec::new();
    for k in 0..10 {
        let mut head: Option<Box<ListNode>> = None;
        for _ in 0..(90000 + 1111 * k) {
            head = Some(Box::new(ListNode { val: next_random(&mut seed) % 1001, next: head }));
        }
        heads.push(head);
    }
    let mut check: i64 = 0;
    for p in 0..30i64 {
        for k in 0..10usize {
            let m = rows[(p as usize + k) % 10];
            let n = 100000 / m;
            let grid = spiral_matrix(m, n, &heads[k]);
            check = (check * 31 + grid[(p % m) as usize][((3 * p + k as i64) % n) as usize] + grid[(m / 2) as usize][(n / 2) as usize] + 2) % 1000000007;
        }
    }
    println!("30 passes over 10 lists in grids of 10^5 cells: checksum {}", check);
    for head in heads {
        drop_list(head);
    }
}
