from simulate_game import play
from pathlib import Path

SOLUTIONS_PATH = "solutions"
RESULT_PATH = "results"
LOG_PATH = "tournament_logs"

Path.mkdir(Path(LOG_PATH), parents=True, exist_ok=True)
Path.mkdir(Path(RESULT_PATH), parents=True, exist_ok=True)

solution_pathes = [path for path in Path(SOLUTIONS_PATH).glob("*")]
solution_names = [solution_path.stem for solution_path in solution_pathes]
solution_exec = list(map(str, solution_pathes))
n = len(solution_pathes)
results = [[(0, 0)] * n for i in range(n)]
diff_sums = [0] * n
for i in range(n):
    for j in range(n):
        if i != j:
            log_path = Path(LOG_PATH) / f"{solution_names[i]}-{solution_names[j]}.txt"
            results[i][j] = play(solution_exec[j], solution_exec[i], log_path)
            diff_sums[i] += results[i][j][0] - results[i][j][1]
            diff_sums[j] -= results[i][j][0] - results[i][j][1]
with open(Path(RESULT_PATH)/"results.txt", "w") as fout:
    for i in range(n):
        fout.write(f"{solution_names[i]} {diff_sums[i]}\n")
    for i in range(n):
        fout.write("\t".join(map(str, results[i])) + '\n')
