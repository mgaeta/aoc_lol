package utils

import (
	"strconv"
	"strings"
)

func GetStrings(data string) []string {
	output := make([]string, 0)

	splitData := strings.Split(data, "\n")

	for i := 0; i < len(splitData); i++ {
		output = append(output, splitData[i])
	}
	if output[len(output)-1] == "" {
		output = output[:len(output)-1]
	}
	return output
}

func GetIntegers(data string) []int {
	output := make([]int, 0)

	splitData := GetStrings(data)

	for i := 0; i < len(splitData); i++ {
		asString := splitData[i]
		asInt, err := strconv.Atoi(asString)
		if err != nil {
			panic(err)
		}
		output = append(output, asInt)
	}
	return output
}

func GetFloats(data string) []float64 {
	output := make([]float64, 0)

	splitData := GetStrings(data)

	for i := 0; i < len(splitData)-1; i++ {
		asString := splitData[i]
		asFloat, err := strconv.ParseFloat(asString, 64)
		if err != nil {
			panic(err)
		}
		output = append(output, asFloat)
	}
	return output
}
