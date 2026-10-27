using System;
using System.Diagnostics;
using System.Globalization;

static class Benchmark
{
    static readonly int benchmark_n = 8;

    static int Solve(int[] board, int row)
    {
        if (row == benchmark_n) return 1;
        int count = 0;
        for (int col = 0; col < benchmark_n; col++)
        {
            bool safe = true;
            for (int prev = 0; prev < row; prev++)
            {
                int delta = row - prev;
                if (board[prev] == col || board[prev] == col - delta || board[prev] == col + delta)
                { safe = false; break; }
            }
            if (safe) { board[row] = col; count += Solve(board, row + 1); }
        }
        return count;
    }

    static int BenchmarkRun()
    {
        int[] board = new int[benchmark_n];
        return Solve(board, 0);
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
