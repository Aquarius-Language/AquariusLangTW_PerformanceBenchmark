using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 80;

    static void Main()
    {
        long benchmark_start = Stopwatch.GetTimestamp();
        int benchmark_result = 0;
        for (int y = 0; y < benchmark_n; y++)
        {
            double ci = 2.0 * y / benchmark_n - 1.0;
            for (int x = 0; x < benchmark_n; x++)
            {
                double cr = 3.0 * x / benchmark_n - 2.0;
                double zr = 0.0, zi = 0.0;
                int count = 0;
                while (count < 60 && zr * zr + zi * zi <= 4.0)
                {
                    double next_r = zr * zr - zi * zi + cr;
                    zi = 2.0 * zr * zi + ci; zr = next_r; count++;
                }
                benchmark_result += count;
            }
        }
        double benchmark_elapsed_ms = (Stopwatch.GetTimestamp() - benchmark_start) * 1000.0 / Stopwatch.Frequency;
        Console.WriteLine("RESULT " + benchmark_result.ToString(CultureInfo.InvariantCulture));
        Console.WriteLine("ELAPSED_MS " + benchmark_elapsed_ms.ToString("R", CultureInfo.InvariantCulture));
    }
}
