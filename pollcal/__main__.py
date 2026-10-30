"""사용법
  python -m pollcal run [--config 설정.json] [--out results] [--reps 100]
  python -m pollcal quick            # 반복 10회로 빠르게 점검
"""
import argparse
from . import config
from .experiments import run_all


def main():
    ap = argparse.ArgumentParser(prog="pollcal", description="여론조사 보정법 비교 프로그램")
    ap.add_argument("cmd", choices=["run", "quick"])
    ap.add_argument("--config"); ap.add_argument("--out", default="results"); ap.add_argument("--reps", type=int)
    a = ap.parse_args()
    cfg = config.load(a.config)
    run_all(cfg, a.out, reps=10 if a.cmd == "quick" else a.reps)


if __name__ == "__main__":
    main()
