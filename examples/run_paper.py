"""Example: Run paper trading simulation."""

from pathlib import Path

from ai_arb_lab.config import DATA_DIR
from ai_arb_lab.data.synthetic import SyntheticMarketGenerator


def main() -> None:
    # Ensure we have data
    data_dir = Path(DATA_DIR)
    if not (data_dir / "orderbook.csv").exists():
        print("Generating sample data...")
        gen = SyntheticMarketGenerator(seed=42, n_venues=2)
        gen.generate_all(data_dir, days=1)

    # Run via CLI
    import subprocess

    result = subprocess.run(
        ["ai-arb-lab", "paper-run", "--data-dir", str(data_dir), "--duration", "60"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit(result.returncode)
    print("Paper run complete. No real orders were sent.")


if __name__ == "__main__":
    main()
