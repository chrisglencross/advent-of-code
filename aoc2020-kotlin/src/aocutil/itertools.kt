package aocutil

fun combinations(values: List<Int>, select: Int) : Sequence<List<Int>> = sequence {
    if (select == 0) {
        yield(emptyList<Int>())
    } else {
        for ((index, value) in values.withIndex()) {
            for (remaining in combinations(values.slice(index + 1 until values.size), select - 1)) {
                val result = mutableListOf(value)
                result.addAll(remaining)
                yield(result)
            }
        }
    }
}