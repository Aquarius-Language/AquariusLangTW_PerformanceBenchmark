using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 10000;

    static int BenchmarkRun()
    {
        bool[] flags = new bool[benchmark_n + 1];
        Array.Fill(flags, true);
        flags[0] = false;
        flags[1] = false;
        int p = 2;
        while (p * p <= benchmark_n)
        {
            if (flags[p])
            {
                int j = p * p;
                while (j <= benchmark_n) { flags[j] = false; j += p; }
            }
            p++;
        }
        int benchmark_result = 0;
        for (int i = 2; i <= benchmark_n; i++) if (flags[i]) benchmark_result++;
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
