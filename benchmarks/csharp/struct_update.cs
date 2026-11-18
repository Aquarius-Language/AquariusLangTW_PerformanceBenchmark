using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.Linq;

sealed class Particle { public int X; public int V; }

static class Benchmark
{
    static readonly int benchmark_n = 1000;
    static readonly int benchmark_warmups = 0;
    static readonly int benchmark_timed_runs = 1;

    // Updates 1000 struct particles through a step function, n calls in all.
    static int Step(Particle p)
    {
        p.X = (p.X + p.V) % 10007;
        return p.X;
    }

    static int BenchmarkRun()
    {
        var particles = new Particle[1000];
        for (int j = 0; j < 1000; j++) particles[j] = new Particle { X = j, V = j % 17 + 1 };
        int total = 0;
        for (int i = 0; i < benchmark_n; i++) total = (total + Step(particles[i % 1000])) % 1000003;
        return total;
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
