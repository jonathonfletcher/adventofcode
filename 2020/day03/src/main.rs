use std::fs::File;
use std::io::{self, BufRead};
use std::vec::Vec;

fn traverse(grid: &Vec<Vec<i32>>, dx: &usize, dy: &usize) -> u32
{
    let (mut x, mut y) = (0, 0);
    let (maxx, maxy) = (grid[0].len(), grid.len());
    let mut count = 0;
    // println!("({}, {})", maxx, maxy);
    while y < maxy {
        count += grid[y][x];
        // println!("({}, {}): {:?}", x, y, grid[y][x]);
        y += dy;        
        x = (x + dx) % maxx;
    }
    // println!("({}, {}): {:?}", x, y, count);
    count as u32
}

fn main() {

    let mut grid: Vec<Vec<i32>> = Vec::new();

    let file = match File::open("input.txt") {
        Ok(file) => file,
        Err(error) => panic!("{}", error)
    };

    for line in io::BufReader::new(file).lines() {
        if let Ok(line) = line {
            grid.push(line.chars()
                .map(|c| { if c == '#' { 1 } else { 0 }})
                .collect());
        }
    }
    // println!("{:?}", grid);

    let (dx, dy) = (3, 1);
    let count = traverse(&grid, &dx, &dy);
    println!("({}, {}): {:?}", dx, dy, count);

    let traverses = vec![(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)];
    let mut count_product = 1;
    for (dx, dy) in traverses.iter() {
        let count = traverse(&grid, dx, dy);
        println!("({}, {}): {:?}", dx, dy, count);
        count_product *= count;
    }
    println!("{:?}", count_product);
}
