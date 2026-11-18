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

    // Counts string keys in a hash: one read and one write per update, 1000 distinct keys.
    static int BenchmarkRun()
    {
        var keys = new string[1000];
        for (int j = 0; j < 1000; j++) keys[j] = "key" + j.ToString(CultureInfo.InvariantCulture);
        var counts = new Dictionary<string, int>();
        for (int i = 0; i < benchmark_n; i++)
        {
            string key = keys[i % 1000];
            counts[key] = counts.GetValueOrDefault(key, 0) + 1;
        }
        return counts.GetValueOrDefault("key7", 0) * 1000 + counts.Count;
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
