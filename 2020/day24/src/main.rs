use std::collections::{VecDeque, HashSet};
use std::fs::File;
use std::io::{self, BufRead, Error};

#[allow(dead_code)]
const AOCDEBUG: bool = true;

type AOCResult = std::result::Result<(), Error>;

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
struct AOCPoint {
    x: i32,
    y: i32,
}

impl AOCPoint {
    pub fn new(x: i32, y: i32) -> Self {
        AOCPoint {
            x: x,
            y: y,
        }
    }
    pub fn neighbours(&self) -> Vec<AOCPoint> {
        let mut neighbours: Vec<AOCPoint> = Vec::new();
        for dx in [-2, 2].iter() {
            neighbours.push(AOCPoint::new(
                self.x + dx,
                self.y + 0,
            ));
        }
        for dx in [-1, 1].iter() {
            for dy in [-1, 1].iter() {
                neighbours.push(AOCPoint::new(
                    self.x + dx,
                    self.y + dy,
                ));
            }
        }
        neighbours
    }

}

struct AOCProcessor {
    source: String,
    flooring: HashSet<AOCPoint>,
}

impl AOCProcessor {
    pub fn new(source: String) -> Self {
        AOCProcessor {
            source: source,
            flooring: HashSet::new(),
        }
    }

    pub fn process(&mut self) -> AOCResult {
        self.initialize();
        let _ = match File::open(&self.source) {
            Ok(file) => {
                for line in io::BufReader::new(file).lines() {
                    let mut p: AOCPoint = AOCPoint { x: 0, y: 0 };
                    if let Ok(line) = line {
                        let mut characters = line.chars().collect::<VecDeque<_>>();
                        while characters.len() > 0 {
                            match characters.pop_front() {
                                Some(val) => match val {
                                    'e' => {
                                        p.x += 2;
                                    }
                                    'w' => {
                                        p.x -= 2;
                                    }
                                    'n' => match characters.pop_front() {
                                        Some(val) => match val {
                                            'e' => {
                                                p.x += 1;
                                                p.y += 1;
                                            }
                                            'w' => {
                                                p.x -= 1;
                                                p.y += 1;
                                            }
                                            _ => {}
                                        },
                                        None => {}
                                    },
                                    's' => match characters.pop_front() {
                                        Some(val) => match val {
                                            'e' => {
                                                p.x += 1;
                                                p.y -= 1;
                                            }
                                            'w' => {
                                                p.x -= 1;
                                                p.y -= 1;
                                            }
                                            _ => {}
                                        },
                                        None => {}
                                    },
                                    _ => {}
                                },
                                None => {}
                            }
                        }
                    }
                    if self.flooring.contains(&p) {
                        self.flooring.remove(&p);
                    } else {
                        self.flooring.insert(p);
                    }
                }
            }
            Err(error) => return Err(error),
        };
        println!("result_a: {:?}", self.flooring.len());
        self.finalize();
        Ok(())
    }

    fn initialize(&mut self) {
        self.flooring.clear();
    }

    fn finalize(&mut self) {
        let mut generation = 0;
        while generation < 100 {
            self.step();
            generation += 1;
            if AOCDEBUG {
                println!("generation:{}, population:{}", generation, self.flooring.len());
            }
        }
        println!("result_b: {:?}", self.flooring.len());
    }

    fn step(&mut self) {
        let mut eval_cells: HashSet<AOCPoint> = HashSet::new();
        let mut new_live_cells: HashSet<AOCPoint> = HashSet::new();

        // collect the cells to evaluate
        for p in &self.flooring.clone() {
            if !eval_cells.contains(p) {
                eval_cells.insert(p.clone());
            }
            for n in p.neighbours() {
                if !eval_cells.contains(&n) {
                    eval_cells.insert(n);
                }
            }
        }

        // Any black tile with zero or more than 2 black tiles
        // immediately adjacent to it is flipped to white.

        // Any white tile with exactly 2 black tiles
        // immediately adjacent to it is flipped to black.

        // iterate through them and decide new population
        for p in eval_cells {
            let mut live_count = 0;
            for n in p.neighbours() {
                if self.flooring.contains(&n) {
                    live_count += 1;
                }
            }
            // println!("{:?} -> {}", p, live_count);
            if self.flooring.contains(&p) {
                if live_count != 0 && live_count <= 2 {
                    new_live_cells.insert(p);
                }
            } else {
                if live_count == 2 {
                    new_live_cells.insert(p);
                }
            }
        }
        self.flooring = new_live_cells;
    }
}

fn main() {
    let mut processor = AOCProcessor::new(String::from("input.txt"));
    match processor.process() {
        Ok(()) => {
            println!("DONE");
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
