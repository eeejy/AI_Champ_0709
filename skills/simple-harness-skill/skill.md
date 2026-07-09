---
name: csv-quality-harness
description: Validate CSV files for required columns, missing values, duplicates, negative amounts, and numeric conversion issues.
---

# CSV Quality Harness

이 스킬은 CSV 파일을 입력받아 품질 검사를 수행하고 결과 보고서를 생성합니다.

## 목적
- 필수 컬럼을 자동으로 확인합니다.
- 결측값과 중복 행을 탐지합니다.
- amount 컬럼의 이상값을 검사합니다.
- result_report.txt를 생성합니다.

## 실행 방식
1. sample.csv 또는 원하는 CSV 파일을 준비합니다.
2. 다음 명령으로 실행합니다.
   ```bash
   python csv_quality_harness.py
   ```
3. 결과는 result_report.txt로 저장됩니다.
