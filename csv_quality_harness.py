import csv
import sys
from pathlib import Path
from typing import List, Dict, Tuple


REQUIRED_COLUMNS = ["id", "name", "amount"]


def read_csv_rows(file_path: Path) -> Tuple[List[Dict[str, str]], List[str]]:
    """CSV 파일을 읽어 헤더와 행을 반환합니다."""
    with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        headers = reader.fieldnames or []
    return rows, headers


def check_required_columns(headers: List[str]) -> List[str]:
    """필수 컬럼이 모두 있는지 확인합니다."""
    return [column for column in REQUIRED_COLUMNS if column not in headers]


def check_missing_values(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    """필수 컬럼의 결측값을 검사합니다."""
    issues = []
    for index, row in enumerate(rows, start=2):
        for column in REQUIRED_COLUMNS:
            value = (row.get(column) or "").strip()
            if value == "":
                issues.append({"row": index, "column": column, "message": "missing value"})
    return issues


def check_duplicate_rows(rows: List[Dict[str, str]]) -> List[Tuple[int, int]]:
    """완전 동일한 행이 있는지 중복 여부를 검사합니다."""
    seen = {}
    duplicates = []
    for index, row in enumerate(rows, start=2):
        row_signature = tuple((key, row.get(key, "")) for key in row.keys())
        if row_signature in seen:
            duplicates.append((seen[row_signature], index))
        else:
            seen[row_signature] = index
    return duplicates


def check_negative_amount(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    """amount 컬럼의 음수 값을 검사합니다."""
    issues = []
    for index, row in enumerate(rows, start=2):
        value = (row.get("amount") or "").strip()
        if value == "":
            continue
        try:
            amount = float(value)
        except ValueError:
            continue
        if amount < 0:
            issues.append({"row": index, "value": value, "message": "negative amount"})
    return issues


def check_numeric_conversion(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    """amount 컬럼이 숫자로 변환 가능한지 검사합니다."""
    issues = []
    for index, row in enumerate(rows, start=2):
        value = (row.get("amount") or "").strip()
        if value == "":
            issues.append({"row": index, "value": value, "message": "empty amount"})
            continue
        try:
            float(value)
        except ValueError:
            issues.append({"row": index, "value": value, "message": "invalid number"})
    return issues


def build_report(file_path: Path, rows: List[Dict[str, str]], headers: List[str]) -> str:
    """검사 결과를 보고서 문자열로 조합합니다."""
    missing_columns = check_required_columns(headers)
    missing_values = check_missing_values(rows)
    duplicate_rows = check_duplicate_rows(rows)
    negative_amounts = check_negative_amount(rows)
    conversion_failures = check_numeric_conversion(rows)

    lines = []
    lines.append("CSV Quality Check Report")
    lines.append("=" * 28)
    lines.append(f"Source File: {file_path.name}")
    lines.append(f"Required Columns: {', '.join(REQUIRED_COLUMNS)}")
    lines.append("")

    if missing_columns:
        lines.append("Status: FAILED")
        lines.append(f"- Missing required columns: {', '.join(missing_columns)}")
    else:
        lines.append("Status: PASSED")
        lines.append("- Missing required columns: None")

    lines.append(f"- Missing values in required columns: {len(missing_values)}")
    if missing_values:
        for item in missing_values:
            lines.append(f"  - Row {item['row']}: {item['column']} is empty")

    lines.append(f"- Duplicate rows: {len(duplicate_rows)}")
    if duplicate_rows:
        for first, second in duplicate_rows:
            lines.append(f"  - Rows {first} and {second} are identical")

    lines.append(f"- Negative amount values: {len(negative_amounts)}")
    if negative_amounts:
        for item in negative_amounts:
            lines.append(f"  - Row {item['row']}: amount={item['value']}")

    lines.append(f"- Numeric conversion failures: {len(conversion_failures)}")
    if conversion_failures:
        for item in conversion_failures:
            lines.append(f"  - Row {item['row']}: amount={item['value']} ({item['message']})")

    return "\n".join(lines) + "\n"


def write_report(output_path: Path, report: str) -> None:
    """결과 보고서를 파일로 저장합니다."""
    output_path.write_text(report, encoding="utf-8")


def main() -> None:
    """메인 실행 함수입니다."""
    input_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("sample.csv").resolve()
    output_path = Path("result_report.txt").resolve()

    if not input_path.exists():
        report = f"CSV file not found: {input_path}\n"
        write_report(output_path, report)
        print(report, end="")
        return

    rows, headers = read_csv_rows(input_path)
    report = build_report(input_path, rows, headers)
    write_report(output_path, report)

    print(report, end="")
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
