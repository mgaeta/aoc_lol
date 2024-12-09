package problems

import (
	"fmt"
	"strconv"
	"strings"
	"y24/src/utils"
)

func constructInitialDiskMap(input string) (map[int]int, []int, int) {
	lookup := make(map[int]int)
	// The top of the list is the first free space [0,1,3,...]
	freeQueue := make([]int, 0)

	lookupIndex := 0
	nextId := 0
	isFree := false
	for _, nextChar := range strings.Split(input, "") {
		nextInt, err := strconv.Atoi(nextChar)
		if err != nil {
			panic(err)
		}

		if isFree {
			for i := 0; i < nextInt; i++ {
				freeQueue = append(freeQueue, lookupIndex)
				lookupIndex += 1
			}
		} else {
			for i := 0; i < nextInt; i++ {
				lookup[lookupIndex] = nextId
				lookupIndex += 1
			}
			nextId += 1
		}
		isFree = !isFree
	}
	return lookup, freeQueue, lookupIndex

}

func printDiskMap(lookup map[int]int, lastIndex int) {
	for i := 0; i < lastIndex; i++ {
		found, ok := lookup[i]
		if !ok {
			fmt.Print(".")
		} else {
			if found > 9 {
				fmt.Print("*")
			} else {
				fmt.Print(found)
			}
		}
	}
	fmt.Println()
}

func cleanup(
	lookup map[int]int,
	freeQueue []int,
	lastIndex int,
	verbose bool,
) []int {
	output := make([]int, 0)
	freeQueueIndex := 0

	for i := 0; i < lastIndex; i++ {
		found, ok := lookup[i]
		if verbose {
			fmt.Println(i, found, ok)
		}
		if ok {
			output = append(output, found)
		} else {
			for {
				if freeQueue[len(freeQueue)-1] == lastIndex-1 {
					freeQueue = freeQueue[:len(freeQueue)-1]
					lastIndex--
				} else {
					break
				}
			}
			next := lookup[lastIndex-1]
			if verbose {
				fmt.Println(freeQueueIndex, freeQueue[freeQueueIndex], next)
			}
			output = append(output, next)
			freeQueueIndex++
			lastIndex--
		}
	}

	return output
}

func calculateCheckSum(input []int, verbose bool) int {
	output := 0
	for i := 0; i < len(input); i++ {
		if verbose {
			fmt.Println(i, "*", input[i])
		}
		output += input[i] * i
	}
	return output
}

func calculateCheckSum2(input map[int]int, lastIndex int, verbose bool) int {
	output := 0
	for i := 0; i < lastIndex; i++ {
		if verbose {
			fmt.Println(i, "*", input[i])
		}
		output += input[i] * i
	}
	return output
}

func Solve9a(data string, verbose bool) string {
	lines := utils.GetStrings(data)
	if verbose {
		for _, line := range lines {
			fmt.Println(line)
		}
	}
	lookup, freeQueue, lookupIndex := constructInitialDiskMap(lines[0])
	printDiskMap(lookup, lookupIndex)
	fmt.Println(freeQueue)
	cleaned := cleanup(lookup, freeQueue, lookupIndex, verbose)
	output := calculateCheckSum(cleaned, verbose)

	return strconv.Itoa(output)
}

func encodeTuple(startIndex int, length int) string {
	return fmt.Sprintf("%d,%d", startIndex, length)
}

func decodeTuple(input string) (int, int, error) {
	parts := strings.Split(input, ",")
	startIndex, err := strconv.Atoi(parts[0])
	if err != nil {
		return 0, 0, err
	}
	length, err := strconv.Atoi(parts[1])
	if err != nil {
		return 0, 0, err
	}
	return startIndex, length, nil
}

func constructInitialDiskMap2(input string, verbose bool) (map[int]int, []string, []string, int) {
	lookup := make(map[int]int)
	// The top of the list is the first free space [0,1,3,...]
	freeQueue := make([]string, 0)
	// REVERSE ORDER
	blockQueue := make([]string, 0)

	lookupIndex := 0
	nextId := 0
	isFree := false
	for _, nextChar := range strings.Split(input, "") {
		nextInt, err := strconv.Atoi(nextChar)
		if err != nil {
			panic(err)
		}

		token := encodeTuple(lookupIndex, nextInt)
		if isFree {
			if verbose {
				fmt.Println("adding to freeQueue", token)
			}
			freeQueue = append(freeQueue, token)
		} else {
			for i := 0; i < nextInt; i++ {
				lookup[lookupIndex+i] = nextId
			}
			// prepend
			blockQueue = append([]string{token}, blockQueue...)

			nextId += 1
		}
		lookupIndex += nextInt
		isFree = !isFree
	}
	return lookup, freeQueue, blockQueue, lookupIndex

}

func cleanup2(
	lookup map[int]int,
	lastIndex int,
	freeQueue []string,
	blockQueue []string,
	verbose bool,
) map[int]int {
	freeQueueIndex := 0
	blockQueueIndex := 0

	for {
		if verbose {
			fmt.Print("freeQueueIndex ", freeQueueIndex, " ")
			fmt.Print("blockQueueIndex ", blockQueueIndex, " ")
			fmt.Print("freeQueue ", freeQueue, " ")
			fmt.Print("blockQueue ", blockQueue, " ")
			fmt.Println()
		}
		if blockQueueIndex == len(blockQueue) {
			break
		}

		nextBlockString := blockQueue[blockQueueIndex]
		nextBlockStart, nextBlockLength, err := decodeTuple(nextBlockString)
		if err != nil {
			panic(err)
		}

		nextFreeString := freeQueue[freeQueueIndex]
		nextFreeStart, nextFreeLength, err := decodeTuple(nextFreeString)
		if err != nil {
			panic(err)
		}

		if freeQueueIndex == len(freeQueue) || nextFreeStart > nextBlockStart {
			blockQueueIndex++
			freeQueueIndex = 0
			continue
		}

		if nextFreeLength < nextBlockLength {
			freeQueueIndex++
			continue
		}

		for i := 0; i < nextBlockLength; i++ {
			lookup[nextFreeStart+i] = lookup[nextBlockStart+i]
			delete(lookup, nextBlockStart+i)
		}
		// don't decapitate, _excise_
		blockQueue = append(blockQueue[:blockQueueIndex], blockQueue[blockQueueIndex+1:]...)
		blockQueueIndex = 0

		remainder := nextFreeLength - nextBlockLength
		if remainder == 0 {
			// don't decapitate, _excise_
			freeQueue = append(freeQueue[:freeQueueIndex], freeQueue[freeQueueIndex+1:]...)
			freeQueueIndex = 0
		} else {
			if verbose {
				fmt.Println("nextFreeStart", nextFreeStart)
				fmt.Println("remainder", remainder)
				fmt.Println("nextFreeLength-remainder", nextFreeLength-remainder)
			}
			freeQueue[freeQueueIndex] = encodeTuple(nextFreeStart+nextBlockLength, remainder)
		}

		freeQueueIndex = 0
		blockQueueIndex = 0

		if verbose {
			printDiskMap(lookup, lastIndex)
		}
	}
	return lookup
}

func Solve9b(data string, verbose bool) string {
	lines := utils.GetStrings(data)
	if verbose {
		for _, line := range lines {
			fmt.Println(line)
		}
	}
	lookup, freeQueue, blockQueue, lastIndex := constructInitialDiskMap2(
		lines[0],
		false,
	)
	printDiskMap(lookup, lastIndex)
	cleaned := cleanup2(
		lookup,
		lastIndex,
		freeQueue,
		blockQueue,
		verbose,
	)
	printDiskMap(cleaned, lastIndex)
	output := calculateCheckSum2(cleaned, lastIndex, false)

	return strconv.Itoa(output)
}
