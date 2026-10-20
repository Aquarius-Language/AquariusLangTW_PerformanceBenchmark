using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 6;

    static int Ack(int m, int n)
    {
        if (m == 0) return n + 1;
        if (n == 0) return Ack(m - 1, 1);
        return Ack(m - 1, Ack(m, n - 1));
    }

    static void Main()
    {
        long benchmark_start = Stopwatch.GetTimestamp();
        int benchmark_result = Ack(3, benchmark_n);
        double benchmark_elapsed_ms = (Stopwatch.GetTimestamp() - benchmark_start) * 1000.0 / Stopwatch.Frequency;
        Console.WriteLine("RESULT " + benchmark_result.ToString(CultureInfo.InvariantCulture));
        Console.WriteLine("ELAPSED_MS " + benchmark_elapsed_ms.ToString("R", CultureInfo.InvariantCulture));
    }
}
