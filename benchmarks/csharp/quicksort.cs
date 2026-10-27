using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 2000;

    static void Sort(int[] a, int lo, int hi)
    {
        int i = lo, j = hi;
        int pivot = a[(lo + hi) / 2];
        while (i <= j)
        {
            while (a[i] < pivot) i++;
            while (a[j] > pivot) j--;
            if (i <= j)
            {
                int tmp = a[i]; a[i] = a[j]; a[j] = tmp; i++; j--;
            }
        }
        if (lo < j) Sort(a, lo, j);
        if (i < hi) Sort(a, i, hi);
    }

    static int BenchmarkRun()
    {
        int[] values = new int[benchmark_n];
        int seed = 42;
        for (int i = 0; i < benchmark_n; i++)
        {
            int raw = seed * 251 + 17;
            seed = raw - raw / 65536 * 65536;
            values[i] = seed;
        }
        Sort(values, 0, benchmark_n - 1);
        int benchmark_result = 0;
        for (int i = 0; i < benchmark_n; i++)
        {
            if (i > 0 && values[i] < values[i - 1]) throw new Exception("Unsorted output");
            benchmark_result += values[i] * (i + 1);
            benchmark_result -= benchmark_result / 1000003 * 1000003;
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
