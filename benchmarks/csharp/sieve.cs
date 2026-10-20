using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 10000;

    static void Main()
    {
        long benchmark_start = Stopwatch.GetTimestamp();
        bool[] flags = Array.Empty<bool>();
        // Resize copies the old array, matching the other scripts' copy-and-append.
        for (int i = 0; i <= benchmark_n; i++)
        {
            Array.Resize(ref flags, i + 1);
            flags[i] = true;
        }
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
        double benchmark_elapsed_ms = (Stopwatch.GetTimestamp() - benchmark_start) * 1000.0 / Stopwatch.Frequency;
        Console.WriteLine("RESULT " + benchmark_result.ToString(CultureInfo.InvariantCulture));
        Console.WriteLine("ELAPSED_MS " + benchmark_elapsed_ms.ToString("R", CultureInfo.InvariantCulture));
    }
}
