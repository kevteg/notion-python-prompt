import argparse
from notionpython import NotionPython

RUN = "run"
CLEAN = "clean"


def init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pynotion",
        usage="%(prog)s [COMMAND]",
        description="Executes the code in the notion page described in the environment variables.",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"{parser.prog} version 0.0.1"
    )
    parser.add_argument(
        "-t", "--token", dest="token", required=True
    )
    parser.add_argument(
        "-p", "--page", dest="page_id", required=True
    )
    parser.add_argument(
        "-c",
        "--command",
        dest="action",
        default=RUN,
        choices=[RUN, CLEAN],
    )
    return parser


def main() -> None:
    parser = init()
    args = parser.parse_args()
    action = args.action
    token = args.token
    page_id = args.page_id
    notion = NotionPython(token, page_id)
    execute_action = {RUN: notion.eval_code, CLEAN: notion.clean_page}
    execute_action[action]()

if __name__ == "__main__":
    main()
