using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 45;
    static readonly int benchmark_warmups = 0;
    static readonly int benchmark_timed_runs = 1;

    static int BenchmarkRun()
    {
        int[] a = new int[benchmark_n * benchmark_n], b = new int[benchmark_n * benchmark_n];
        for (int i = 0; i < benchmark_n; i++)
        {
            for (int j = 0; j < benchmark_n; j++)
            {
                int x = i + j, y = i * 2 + j;
                int index = i * benchmark_n + j;
                a[index] = x - x / 7 * 7;
                b[index] = y - y / 5 * 5;
            }
        }
        int benchmark_result = 0;
        for (int i = 0; i < benchmark_n; i++)
        {
            for (int j = 0; j < benchmark_n; j++)
            {
                int total = 0;
                for (int k = 0; k < benchmark_n; k++) total += a[i * benchmark_n + k] * b[k * benchmark_n + j];
                benchmark_result += total;
            }
        }
        return benchmark_result;
    }

    static void Main()
    {
        // Untimed in-process warm-up runs, then timed runs; the harness substitutes both counts.
        for (int benchmark_warmup = 0; benchmark_warmup < benchmark_warmups; benchmark_warmup++) BenchmarkRun();
        for (int benchmark_round = 0; benchmark_round < benchmark_timed_runs; benchmark_round++)
        {
            long benchmark_start = Stopwatch.GetTimestamp();
            int benchmark_result = BenchmarkRun();
            double benchmark_elapsed_ms = (Stopwatch.GetTimestamp() - benchmark_start) * 1000.0 / Stopwatch.Frequency;
            Console.WriteLine("RESULT " + benchmark_result.ToString(CultureInfo.InvariantCulture));
            Console.WriteLine("ELAPSED_MS " + benchmark_elapsed_ms.ToString("R", CultureInfo.InvariantCulture));
        }
    }
}
