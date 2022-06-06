import sys
from datetime import datetime

from comparer.cli import Cli


# just main entry point
def run_cli() -> int:
    args = sys.argv[1:]
    cli_app = Cli.new_cli_app(args)
    return cli_app.run()


if __name__ == "__main__":
    start = datetime.now()
    print(f"Comparing started @ {start}")
    exit_code = run_cli()
    end = datetime.now()
    print(f"Comparing finished @ {end}")
    print(f"Comparing took: {end-start}")
    sys.exit(exit_code)
