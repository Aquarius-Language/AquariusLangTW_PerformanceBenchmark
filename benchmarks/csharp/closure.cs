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

    // Maps an array with a function literal, then calls a closure that updates a captured variable n times.
    static int BenchmarkRun()
    {
        int[] doubled = Enumerable.Repeat(1, benchmark_n).Select(x => x * 2).ToArray();
        int total = 0;
        Action<int> add = value => { total = (total + value) % 1000003; };
        for (int i = 0; i < benchmark_n; i++) add(doubled[i] + i % 3);
        return total;
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
