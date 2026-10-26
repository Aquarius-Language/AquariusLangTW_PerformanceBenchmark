using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 12;
    static readonly object Zero = 0;

    static object[] Build(int depth)
    {
        if (depth == 0) return new object[] { Zero, Zero };
        return new object[] { Build(depth - 1), Build(depth - 1) };
    }

    static int Check(object[] tree, int depth)
    {
        if (depth == 0) return 1;
        return 1 + Check((object[])tree[0], depth - 1) + Check((object[])tree[1], depth - 1);
    }

    static void Main()
    {
        long benchmark_start = Stopwatch.GetTimestamp();
        int benchmark_result = 0;
        for (int i = 0; i < 8; i++)
        {
            object[] tree = Build(benchmark_n);
            benchmark_result += Check(tree, benchmark_n);
        }
        double benchmark_elapsed_ms = (Stopwatch.GetTimestamp() - benchmark_start) * 1000.0 / Stopwatch.Frequency;
        Console.WriteLine("RESULT " + benchmark_result.ToString(CultureInfo.InvariantCulture));
        Console.WriteLine("ELAPSED_MS " + benchmark_elapsed_ms.ToString("R", CultureInfo.InvariantCulture));
    }
}
