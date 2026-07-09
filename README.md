# CSV Quality Harness

이 저장소는 CSV 파일의 품질을 자동으로 검사하는 간단한 하네스 스킬 예시입니다.

## 포함된 내용
- CSV 품질 검사 스크립트: csv_quality_harness.py
- 샘플 입력 파일: sample.csv
- 검사 결과 예시: result_report.txt
- 스킬 설명 문서: skills/simple-harness-skill/skill.md

## 주요 검사 항목
- 필수 컬럼 존재 여부
- 필수 컬럼 결측값 여부
- 완전 동일 행 중복 여부
- amount 컬럼 음수 여부
- 숫자 변환 실패 여부

## 실행 방법
```bash
python csv_quality_harness.py
```

다른 CSV 파일도 실행할 수 있습니다.
```bash
python csv_quality_harness.py your_file.csv
```
