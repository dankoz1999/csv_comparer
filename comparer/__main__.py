import sys
from datetime import datetime

from ports.cli import Cli


# just main entry point
def run_cli() -> int:
    args = sys.argv[1:]
    cli_app = Cli.new_cli_app(args)
    return cli_app.run()


if __name__ == "__main__":
    start = datetime.now()
    print(f"Creating headers started @ {start}")
    exit_code = run_cli()
    end = datetime.now()
    print(f"Creating headers finished @ {end}")
    print(f"Creating headers took: {end-start}")
    sys.exit(exit_code)
