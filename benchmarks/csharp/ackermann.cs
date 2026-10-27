using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 6;
    static readonly int benchmark_warmups = 0;
    static readonly int benchmark_timed_runs = 1;

    static int Ack(int m, int n)
    {
        if (m == 0) return n + 1;
        if (n == 0) return Ack(m - 1, 1);
        return Ack(m - 1, Ack(m, n - 1));
    }

    static int BenchmarkRun()
    {
        return Ack(3, benchmark_n);
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
