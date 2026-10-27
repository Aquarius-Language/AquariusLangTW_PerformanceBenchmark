using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 10000;

    static int BenchmarkRun()
    {
        int benchmark_result = 0;
        for (int start = 1; start <= benchmark_n; start++)
        {
            int value = start;
            while (value != 1)
            {
                int half = value / 2;
                if (half * 2 == value) value = half;
                else value = value * 3 + 1;
                benchmark_result++;
            }
        }
        return benchmark_result;
    }

    static void Main()
    {
        // Untimed warm-up runs, identical in every language.
        for (int benchmark_warmup = 0; benchmark_warmup < 3; benchmark_warmup++) BenchmarkRun();
        long benchmark_start = Stopwatch.GetTimestamp();
        int benchmark_result = BenchmarkRun();
        double benchmark_elapsed_ms = (Stopwatch.GetTimestamp() - benchmark_start) * 1000.0 / Stopwatch.Frequency;
        Console.WriteLine("RESULT " + benchmark_result.ToString(CultureInfo.InvariantCulture));
        Console.WriteLine("ELAPSED_MS " + benchmark_elapsed_ms.ToString("R", CultureInfo.InvariantCulture));
    }
}
