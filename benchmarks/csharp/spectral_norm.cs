using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 60;

    static double Element(int i, int j)
    {
        int s = i + j;
        return 1.0 / (s * (s + 1) / 2 + i + 1);
    }

    static void Multiply(double[] src, double[] dst, bool transpose)
    {
        for (int i = 0; i < benchmark_n; i++)
        {
            double total = 0.0;
            for (int j = 0; j < benchmark_n; j++)
            {
                double coefficient = transpose ? Element(j, i) : Element(i, j);
                total += coefficient * src[j];
            }
            dst[i] = total;
        }
    }

    static double BenchmarkRun()
    {
        double[] u = new double[benchmark_n], v = new double[benchmark_n], temp = new double[benchmark_n];
        Array.Fill(u, 1.0);
        for (int iteration = 0; iteration < 10; iteration++)
        {
            Multiply(u, temp, false); Multiply(temp, v, true);
            Multiply(v, temp, false); Multiply(temp, u, true);
        }
        double uv = 0.0, vv = 0.0;
        for (int i = 0; i < benchmark_n; i++) { uv += u[i] * v[i]; vv += v[i] * v[i]; }
        return uv / vv;
    }

    static void Main()
    {
        // Untimed warm-up runs, identical in every language.
        for (int benchmark_warmup = 0; benchmark_warmup < 3; benchmark_warmup++) BenchmarkRun();
        long benchmark_start = Stopwatch.GetTimestamp();
        double benchmark_result = BenchmarkRun();
        double benchmark_elapsed_ms = (Stopwatch.GetTimestamp() - benchmark_start) * 1000.0 / Stopwatch.Frequency;
        Console.WriteLine("RESULT " + benchmark_result.ToString(CultureInfo.InvariantCulture));
        Console.WriteLine("ELAPSED_MS " + benchmark_elapsed_ms.ToString("R", CultureInfo.InvariantCulture));
    }
}
