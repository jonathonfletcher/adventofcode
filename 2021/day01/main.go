package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
)

func part1(scanner *bufio.Scanner) uint64 {

	var prevDepth uint64

	var lineCount = 0
	var countIncrease uint64 = 0

	for scanner.Scan() {
		line := scanner.Text()
		newDepth, _ := strconv.ParseUint(line, 10, 64)
		lineCount++

		if lineCount > 1 && newDepth > prevDepth {
			countIncrease += 1
		}
		prevDepth = newDepth
		// log.Println(line, newDepth, countIncrease)
	}

	return countIncrease
}

func part2(scanner *bufio.Scanner) uint64 {

	lookBack := 4
	var valStore = make([]uint64, lookBack)
	for i := 0; i < lookBack; i++ {
		valStore[i] = 0
	}

	var lineCount = 0
	var countIncrease uint64 = 0

	for scanner.Scan() {
		var pSum uint64 = 0
		for i := 0; i < lookBack; i++ {
			pSum += valStore[i]
		}

		line := scanner.Text()
		newVal, _ := strconv.ParseUint(line, 10, 64)
		lineCount++

		valStore[(lineCount-1)%lookBack] = newVal
		valStore[lineCount%lookBack] = 0

		var cSum uint64 = 0
		for i := 0; i < lookBack; i++ {
			cSum += valStore[i]
		}

		if lineCount >= lookBack && cSum > pSum {
			countIncrease++
		}
		// log.Println(cSum, pSum, countIncrease, valStore)

	}

	return countIncrease
}

func main() {

	{
		inFile, err := os.Open("part1.txt")
		if err != nil {
			log.Fatal("cannot open input")
		} else {
			scanner := bufio.NewScanner(inFile)
			scanner.Split(bufio.ScanLines)
			partAnswer := part1(scanner)
			log.Println("part1:", partAnswer)
			inFile.Close()
		}
	}

	{
		inFile, err := os.Open("part1.txt")
		if err != nil {
			log.Fatal("cannot open input")
		} else {
			scanner := bufio.NewScanner(inFile)
			scanner.Split(bufio.ScanLines)
			partAnswer := part2(scanner)
			log.Println("part2:", partAnswer)
			inFile.Close()
		}
	}

}
