from __future__ import annotations

from pathlib import Path


def copy_if_exists(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    content = src.read_text(encoding="utf-8")
    if not content.strip():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    copied = []

    if copy_if_exists(Path("working/generated-flow.md"), Path("outputs/diagrams/generated-flow.md")):
        copied.append("outputs/diagrams/generated-flow.md")
    if copy_if_exists(Path("working/generated-testcases.md"), Path("outputs/testcases/testcases.md")):
        copied.append("outputs/testcases/testcases.md")
    if copy_if_exists(Path("working/generated-api-contracts.md"), Path("outputs/contracts/api-contracts.md")):
        copied.append("outputs/contracts/api-contracts.md")
    if copy_if_exists(Path("working/api-contracts/openapi.yaml"), Path("outputs/contracts/openapi.yaml")):
        copied.append("outputs/contracts/openapi.yaml")

    if copied:
        print("Copied derived artifacts:")
        for item in copied:
            print(f"- {item}")
    else:
        print("No derived artifacts found to copy.")


if __name__ == "__main__":
    main()
