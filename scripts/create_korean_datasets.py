#!/usr/bin/env python3
"""
한국어 데이터셋 생성 스크립트
Korean Dataset Generation Script

This script creates sample Korean datasets for Heretic abliteration.
이 스크립트는 Heretic abliteration을 위한 샘플 한국어 데이터셋을 생성합니다.

Usage:
    python scripts/create_korean_datasets.py
"""

from datasets import Dataset
import os
import csv


def load_prompts_from_csv(file_path):
    """CSV 파일에서 프롬프트 로드 / Load prompts from CSV file"""
    prompts = []
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompts.append(row["prompt"])
    return prompts


def create_datasets():
    """데이터셋 생성 및 저장 / Create and save datasets"""

    print("=" * 60)
    print("한국어 데이터셋 생성 중...")
    print("Creating Korean datasets...")
    print("=" * 60)

    # CSV 파일 경로
    harmless_csv = "./data/korean_harmless_prompts.csv"
    harmful_csv = "./data/korean_harmful_prompts.csv"

    # CSV 파일에서 프롬프트 로드
    print("\n[0/2] CSV 파일에서 프롬프트 로딩 중...")
    print("       Loading prompts from CSV files...")

    harmless_prompts = load_prompts_from_csv(harmless_csv)
    harmful_prompts = load_prompts_from_csv(harmful_csv)

    print(f"       ✓ 무해한 프롬프트: {len(harmless_prompts)}개")
    print(f"       ✓ Harmless prompts: {len(harmless_prompts)} items")
    print(f"       ✓ 유해한 프롬프트: {len(harmful_prompts)}개")
    print(f"       ✓ Harmful prompts: {len(harmful_prompts)} items")

    # 디렉토리 확인
    os.makedirs("./datasets/korean_harmless", exist_ok=True)
    os.makedirs("./datasets/korean_harmful", exist_ok=True)

    # 무해한 프롬프트 데이터셋 생성
    print(f"\n[1/2] 무해한 프롬프트 데이터셋 생성 중...")
    print(f"       Creating harmless prompts dataset...")
    print(f"       항목 수 / Number of items: {len(harmless_prompts)}")

    harmless_dataset = Dataset.from_dict({"text": harmless_prompts})
    harmless_dataset.save_to_disk("./datasets/korean_harmless")
    print(f"       ✓ 저장 완료: ./datasets/korean_harmless")
    print(f"       ✓ Saved to: ./datasets/korean_harmless")

    # 유해한 프롬프트 데이터셋 생성
    print(f"\n[2/2] 유해한 프롬프트 데이터셋 생성 중...")
    print(f"       Creating harmful prompts dataset...")
    print(f"       항목 수 / Number of items: {len(harmful_prompts)}")

    harmful_dataset = Dataset.from_dict({"text": harmful_prompts})
    harmful_dataset.save_to_disk("./datasets/korean_harmful")
    print(f"       ✓ 저장 완료: ./datasets/korean_harmful")
    print(f"       ✓ Saved to: ./datasets/korean_harmful")

    print("\n" + "=" * 60)
    print("✓ 데이터셋 생성 완료!")
    print("✓ Datasets created successfully!")
    print("=" * 60)

    print("\n다음 단계:")
    print("Next steps:")
    print("  1. config.korean.toml을 편집하여 로컬 데이터셋 사용:")
    print("     Edit config.korean.toml to use local datasets:")
    print("     [good_prompts]")
    print("     dataset = './datasets/korean_harmless'")
    print("     [bad_prompts]")
    print("     dataset = './datasets/korean_harmful'")
    print()
    print("  2. Heretic 실행:")
    print("     Run Heretic:")
    print("     heretic --config config.korean.toml --model <your-model>")
    print()
    print("  3. 더 많은 프롬프트를 추가하려면:")
    print("     To add more prompts:")
    print("     - data/korean_harmless_prompts.csv 편집 (엑셀/구글 시트 사용 가능)")
    print("     - data/korean_harmful_prompts.csv 편집 (엑셀/구글 시트 사용 가능)")
    print("     - 이 스크립트 재실행")
    print()


if __name__ == "__main__":
    create_datasets()
