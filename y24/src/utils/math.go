package utils

import "math"

func SumIntegers(inputs []int) int {
	output := 0
	for _, input := range inputs {
		output += input
	}
	return output
}

func SumFloats(inputs []float64) float64 {
	output := 0.0
	for _, input := range inputs {
		output += input
	}
	return output
}

func MaxInteger(inputs []int) int {
	output := math.MinInt
	for _, input := range inputs {
		if output < input {
			output = input
		}
	}
	return output
}

func MaxFloat(inputs []float64) float64 {
	output := -math.MaxFloat64
	for _, input := range inputs {
		if output < input {
			output = input
		}
	}
	return output
}

func Abs(a int) int {
	if a >= 0 {
		return a
	}
	return -a
}
