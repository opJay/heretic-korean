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


def split_prompts(prompts, eval_size=100):
    """
    프롬프트를 train/eval로 분리
    Split prompts into train and eval sets

    Args:
        prompts: 프롬프트 리스트 / List of prompts
        eval_size: Evaluation 데이터 개수 (기본 100개) / Number of evaluation samples (default 100)

    Returns:
        (train_prompts, eval_prompts)
    """
    total = len(prompts)

    if total <= eval_size:
        print(f"       ⚠ 경고: 전체 데이터({total}개)가 평가 데이터 크기({eval_size}개)보다 작습니다.")
        print(f"       ⚠ Warning: Total data ({total}) is smaller than eval size ({eval_size}).")
        print(f"       → 80/20 비율로 분리합니다 / Using 80/20 split")
        eval_size = max(1, int(total * 0.2))

    train_prompts = prompts[:-eval_size]
    eval_prompts = prompts[-eval_size:]

    return train_prompts, eval_prompts


def create_datasets(eval_size=100):
    """
    데이터셋 생성 및 저장 / Create and save datasets

    Args:
        eval_size: Evaluation 데이터 개수 (기본 100개) / Number of evaluation samples (default 100)
    """

    print("=" * 60)
    print("한국어 데이터셋 생성 중...")
    print("Creating Korean datasets...")
    print("=" * 60)

    # CSV 파일 경로
    harmless_csv = "./data/korean_harmless_prompts.csv"
    harmful_csv = "./data/korean_harmful_prompts.csv"

    # CSV 파일 존재 여부 확인
    if not os.path.exists(harmless_csv):
        print(f"\n❌ 오류: {harmless_csv} 파일을 찾을 수 없습니다!")
        print(f"❌ Error: {harmless_csv} not found!")
        return

    if not os.path.exists(harmful_csv):
        print(f"\n❌ 오류: {harmful_csv} 파일을 찾을 수 없습니다!")
        print(f"❌ Error: {harmful_csv} not found!")
        return

    # CSV 파일에서 프롬프트 로드
    print("\n[1/4] CSV 파일에서 프롬프트 로딩 중...")
    print("       Loading prompts from CSV files...")

    harmless_prompts = load_prompts_from_csv(harmless_csv)
    harmful_prompts = load_prompts_from_csv(harmful_csv)

    print(f"       ✓ 무해한 프롬프트: {len(harmless_prompts)}개")
    print(f"       ✓ Harmless prompts: {len(harmless_prompts)} items")
    print(f"       ✓ 유해한 프롬프트: {len(harmful_prompts)}개")
    print(f"       ✓ Harmful prompts: {len(harmful_prompts)} items")

    # Train/Eval 분리
    print(f"\n[2/4] 데이터셋 분리 중 (Eval: {eval_size}개)...")
    print(f"       Splitting datasets (Eval size: {eval_size})...")

    harmless_train, harmless_eval = split_prompts(harmless_prompts, eval_size)
    harmful_train, harmful_eval = split_prompts(harmful_prompts, eval_size)

    print(f"       ✓ Harmless - Train: {len(harmless_train)}개, Eval: {len(harmless_eval)}개")
    print(f"       ✓ Harmful - Train: {len(harmful_train)}개, Eval: {len(harmful_eval)}개")

    # 디렉토리 생성
    print("\n[3/4] 디렉토리 생성 중...")
    print("       Creating directories...")

    os.makedirs("./datasets/korean_harmless_train", exist_ok=True)
    os.makedirs("./datasets/korean_harmless_eval", exist_ok=True)
    os.makedirs("./datasets/korean_harmful_train", exist_ok=True)
    os.makedirs("./datasets/korean_harmful_eval", exist_ok=True)

    # 데이터셋 생성 및 저장
    print("\n[4/4] 데이터셋 저장 중...")
    print("       Saving datasets...")

    datasets_info = [
        ("harmless_train", harmless_train),
        ("harmless_eval", harmless_eval),
        ("harmful_train", harmful_train),
        ("harmful_eval", harmful_eval),
    ]

    for name, prompts in datasets_info:
        dataset = Dataset.from_dict({"text": prompts})
        output_path = f"./datasets/korean_{name}"
        dataset.save_to_disk(output_path)
        print(f"       ✓ {name}: {len(prompts)}개 → {output_path}")

    print("\n" + "=" * 60)
    print("✓ 데이터셋 생성 완료!")
    print("✓ Datasets created successfully!")
    print("=" * 60)

    print("\n다음 단계:")
    print("Next steps:")
    print("  1. config.korean.toml을 편집하여 로컬 데이터셋 사용:")
    print("     Edit config.korean.toml to use local datasets:")
    print("     [good_prompts]")
    print("     dataset = './datasets/korean_harmless_train'")
    print("     [bad_prompts]")
    print("     dataset = './datasets/korean_harmful_train'")
    print("     [good_evaluation_prompts]")
    print("     dataset = './datasets/korean_harmless_eval'")
    print("     [bad_evaluation_prompts]")
    print("     dataset = './datasets/korean_harmful_eval'")
    print()
    print("  2. Heretic 실행:")
    print("     Run Heretic:")
    print("     heretic --config config.korean.toml --model <your-model>")
    print()
    print("  3. 더 많은 프롬프트를 추가하려면:")
    print("     To add more prompts:")
    print("     - data/korean_harmless_prompts.csv 편집")
    print("     - data/korean_harmful_prompts.csv 편집")
    print("     - 이 스크립트 재실행")
    print()


if __name__ == "__main__":
    create_datasets()
