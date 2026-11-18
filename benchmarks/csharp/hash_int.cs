using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.Linq;


static class Benchmark
{
    static readonly int benchmark_n = 1000;
    static readonly int benchmark_warmups = 0;
    static readonly int benchmark_timed_runs = 1;

    // Fills a hash with n / 5 integer keys, then reads n of them.
    static int BenchmarkRun()
    {
        int size = benchmark_n / 5;
        var table = new Dictionary<int, int>();
        for (int i = 0; i < size; i++) table[i * 7] = i;
        int sum = 0;
        for (int i = 0; i < benchmark_n; i++) sum = (sum + table[((i * 13) % size) * 7]) % 1000003;
        return sum;
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
