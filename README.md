# Heretic: 언어 모델의 완전 자동 검열 제거

Heretic은 트랜스포머 기반 언어 모델에서 검열(일명 "안전성 정렬")을 비용이 많이 드는 후처리 없이 제거하는 도구입니다.
방향성 제거(Directional Ablation), 일명 "abliteration" ([Arditi et al. 2024](https://arxiv.org/abs/2406.11717))의
고급 구현과 [Optuna](https://optuna.org/) 기반 TPE 파라미터 최적화를 결합했습니다.

이러한 접근 방식을 통해 Heretic은 **완전히 자동으로** 작동합니다. Heretic은
거부 응답 횟수와 원본 모델로부터의 KL divergence를 동시에 최소화하여 고품질의 abliteration 파라미터를 찾습니다.
그 결과 원본 모델의 지능을 최대한 보존하면서 검열을 제거한 모델을 얻을 수 있습니다.
Heretic을 사용하는 데 트랜스포머 내부 구조에 대한 이해가 필요하지 않습니다.
실제로 명령줄 프로그램을 실행할 수 있는 사람이라면 누구나 Heretic을 사용하여 언어 모델의 검열을 제거할 수 있습니다.

<img width="650" height="715" alt="스크린샷" src="https://github.com/user-attachments/assets/d71a5efa-d6be-4705-a817-63332afb2d15" />

&nbsp;

기본 설정으로 무감독 실행할 경우, Heretic은 인간 전문가가 수동으로 만든 abliteration과
비슷한 품질의 검열 제거 모델을 생성할 수 있습니다:

| 모델 | "유해한" 프롬프트에 대한 거부 횟수 | "무해한" 프롬프트에 대한 원본 모델과의 KL divergence |
| :--- | ---: | ---: |
| [google/gemma-3-12b-it](https://huggingface.co/google/gemma-3-12b-it) (원본) | 97/100 | 0 *(정의상)* |
| [mlabonne/gemma-3-12b-it-abliterated-v2](https://huggingface.co/mlabonne/gemma-3-12b-it-abliterated-v2) | 3/100 | 1.04 |
| [huihui-ai/gemma-3-12b-it-abliterated](https://huggingface.co/huihui-ai/gemma-3-12b-it-abliterated) | 3/100 | 0.45 |
| **[p-e-w/gemma-3-12b-it-heretic](https://huggingface.co/p-e-w/gemma-3-12b-it-heretic) (Heretic 버전)** | **3/100** | **0.16** |

인간의 노력 없이 생성된 Heretic 버전은 다른 abliteration과 동일한 수준의 거부 억제를 달성하지만,
훨씬 낮은 KL divergence를 보여 원본 모델의 능력에 대한 손상이 적음을 나타냅니다.
*(Heretic의 내장 평가 기능을 사용하여 이 수치를 재현할 수 있습니다.
예: `heretic --model google/gemma-3-12b-it --evaluate-model p-e-w/gemma-3-12b-it-heretic`.
정확한 값은 플랫폼과 하드웨어에 따라 다를 수 있습니다.
위 표는 RTX 5090에서 PyTorch 2.8을 사용하여 작성되었습니다.)*

Heretic은 대부분의 dense 모델(다수의 멀티모달 모델 포함)과
여러 MoE 아키텍처를 지원합니다. 아직 SSM/하이브리드 모델,
불균일한 레이어를 가진 모델, 특정 새로운 어텐션 시스템은 지원하지 않습니다.

Heretic을 사용하여 검열이 제거된 모델 컬렉션을
[Hugging Face에서](https://huggingface.co/collections/p-e-w/the-bestiary) 확인할 수 있습니다.


## 사용법

### 환경 준비

하드웨어에 적합한 PyTorch 2.2+ 버전이 설치된 Python 3.10+ 환경을 준비하세요.

### 설치

**이 포크는 한국어와 영어 모델을 모두 지원합니다.** GitHub에서 직접 설치하세요:

```bash
pip install git+https://github.com/opJay/heretic-korean.git@korean
```

또는 개발 모드로 설치:

```bash
git clone https://github.com/opJay/heretic-korean.git
cd heretic-korean
pip install -e .
```

### 업데이트

이미 heretic-korean을 설치한 경우, 다음 방법으로 최신 버전으로 업데이트하세요:

**GitHub에서 직접 설치한 경우:**

```bash
pip install --upgrade git+https://github.com/opJay/heretic-korean.git@korean
```

**개발 모드로 설치한 경우:**

```bash
cd heretic-korean
git pull origin korean
# 개발 모드(-e)로 설치되어 있으면 코드 변경사항이 자동으로 반영됩니다
# 필요한 경우에만 재설치:
pip install -e .
```

### 한국어 모델 사용

한국어 모델의 경우 한국어 설정 파일(`config.korean.toml`)을 사용하세요:

```bash
heretic --config config.korean.toml --model beomi/Llama-3-Open-Ko-8B
```

**한국어 거부 패턴 지원:**
- "죄송합니다", "할 수 없습니다"
- "AI로서", "언어 모델로서"
- "불법", "유해", "부적절", "윤리적" 등

**현재 상태:**
- ✅ 한국어 거부 패턴 100% 지원 ([`config.korean.toml`](config.korean.toml))
- ⚠️ 학습 데이터는 기본적으로 영어 사용 (다국어 모델에도 효과적)
- 📦 한국어 데이터셋 준비 기능 제공 (아래 참조)

### 한국어 데이터셋 준비 (선택사항)

한국어 프롬프트로 학습하면 더 나은 결과를 얻을 수 있습니다.

#### 로컬 데이터셋 생성

```bash
# 샘플 한국어 데이터셋 생성
python scripts/create_korean_datasets.py

# config.korean.toml 편집하여 로컬 데이터셋 사용
# [good_prompts]
# dataset = "./datasets/korean_harmless"
# [bad_prompts]
# dataset = "./datasets/korean_harmful"
```

#### 자신만의 데이터셋 추가

1. `scripts/create_korean_datasets.py` 편집
2. `harmless_prompts`와 `harmful_prompts` 리스트에 프롬프트 추가
3. 스크립트 재실행

#### Hugging Face로 공유 (향후)

데이터셋이 충분히 검증되면 Hugging Face에 업로드하여 공유할 수 있습니다:

```bash
# 데이터셋 업로드 (예시)
huggingface-cli login
# ... 업로드 과정
```

### 영어 및 다국어 모델 사용

영어 모델은 기본 설정을 사용하세요:

```bash
heretic --model Qwen/Qwen3-4B-Instruct-2507
```

모델 이름을 검열을 제거하려는 모델로 교체하세요.

### 상세 설정

프로세스는 완전히 자동이며 설정이 필요하지 않습니다. 하지만
Heretic은 더 세밀한 제어를 위해 변경할 수 있는 다양한 설정 파라미터를 제공합니다.

- **명령줄 옵션**: `heretic --help`
- **설정 파일**: [`config.default.toml`](config.default.toml) (영어) 또는 `config.korean.toml` (한국어)

### 실행 시간

프로그램 실행 시작 시 Heretic은 시스템을 벤치마크하여
사용 가능한 하드웨어를 최대한 활용하기 위한 최적의 배치 크기를 결정합니다.

**참고 시간:** RTX 3090에서 기본 설정으로 Llama-3.1-8B의 검열을 제거하는 데 약 45분이 걸립니다.

### 완료 후 옵션

Heretic이 모델의 검열 제거를 완료한 후, 다음 옵션 중 선택할 수 있습니다:
- 모델 로컬 저장
- Hugging Face에 업로드
- 대화형 테스트 (채팅)
- 또는 이들의 조합


## 작동 원리

Heretic은 방향성 제거(directional ablation)의 파라미터화된 변형을 구현합니다.
지원되는 각 트랜스포머 컴포넌트(현재는 attention out-projection과
MLP down-projection)에 대해 각 트랜스포머 레이어에서 관련 행렬을 식별하고,
관련 "거부 방향"에 대해 직교화하여 해당 행렬과의 곱셈 결과에서
그 방향의 표현을 억제합니다.

거부 방향은 "유해한" 프롬프트와 "무해한" 프롬프트 예시에 대한
첫 번째 토큰 residual의 평균 차이로 각 레이어에 대해 계산됩니다.

Ablation 프로세스는 여러 최적화 가능한 파라미터로 제어됩니다:

* `direction_index`: 거부 방향의 인덱스, 또는 각 레이어가 해당 레이어와
  연관된 거부 방향을 사용하여 ablate되어야 함을 나타내는 특수 값 `per layer`.
* `max_weight`, `max_weight_position`, `min_weight`, `min_weight_distance`:
  각 컴포넌트에 대해 이 파라미터들은 레이어에 걸친 ablation 가중치 커널의
  모양과 위치를 설명합니다. 다음 다이어그램은 이를 설명합니다:

<img width="800" height="500" alt="설명" src="https://github.com/user-attachments/assets/82e4b84e-5a82-4faf-b918-ac642f9e4892" />

&nbsp;

기존 abliteration 시스템에 대한 Heretic의 주요 혁신 사항은 다음과 같습니다:

* Ablation 가중치 커널의 형태가 매우 유연하며, 자동 파라미터 최적화와 결합되어
  순응성/품질 트레이드오프를 개선할 수 있습니다.
  비상수 ablation 가중치는 이전에 Maxime Labonne이
  [gemma-3-12b-it-abliterated-v2](https://huggingface.co/mlabonne/gemma-3-12b-it-abliterated-v2)에서 탐구했습니다.
* 거부 방향 인덱스는 정수가 아닌 부동소수점입니다. 비정수 값의 경우
  가장 가까운 두 거부 방향 벡터가 선형 보간됩니다.
  이는 평균 차이 계산으로 식별된 방향 이상의 광대한 추가 방향 공간을 열어주며,
  종종 최적화 프로세스가 개별 레이어에 속한 것보다 더 나은 방향을 찾을 수 있게 합니다.
* Ablation 파라미터는 각 컴포넌트에 대해 별도로 선택됩니다.
  MLP 개입이 attention 개입보다 모델에 더 큰 손상을 주는 경향이 있어,
  서로 다른 ablation 가중치를 사용하면 추가 성능을 얻을 수 있습니다.


## 선행 연구

다음과 같은 abliteration 기술의 공개 구현을 알고 있습니다:

* [AutoAbliteration](https://huggingface.co/posts/mlabonne/714992455492422)
* [abliterator.py](https://github.com/FailSpy/abliterator)
* [wassname's Abliterator](https://github.com/wassname/abliterator)
* [ErisForge](https://github.com/Tsadoq/ErisForge)
* [Removing refusals with HF Transformers](https://github.com/Sumandora/remove-refusals-with-transformers)
* [deccp](https://github.com/AUGMXNT/deccp)

참고로 Heretic은 처음부터 작성되었으며, 위 프로젝트들의 코드를 재사용하지 않습니다.


## 감사의 말

Heretic의 개발은 다음 자료들을 참고했습니다:

* [원본 abliteration 논문 (Arditi et al. 2024)](https://arxiv.org/abs/2406.11717)
* [Maxime Labonne의 abliteration 관련 글](https://huggingface.co/blog/mlabonne/abliteration),
  그리고 그의 abliterated 모델 카드의 일부 세부사항 (위 참조)
* [Jim Lai의 "projected abliteration" 관련 글](https://huggingface.co/blog/grimjim/projected-abliteration)


## 인용

연구에 Heretic을 사용하는 경우 다음 BibTeX 항목을 사용하여 인용해 주세요:

```bibtex
@misc{heretic,
  author = {Weidmann, Philipp Emanuel},
  title = {Heretic: Fully automatic censorship removal for language models},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/p-e-w/heretic}}
}
```


## 라이선스

Copyright &copy; 2025  Philipp Emanuel Weidmann (<pew@worldwidemann.com>)

이 프로그램은 자유 소프트웨어입니다. Free Software Foundation이 발행한
GNU Affero General Public License 버전 3 또는 (선택에 따라) 그 이후 버전의
조건에 따라 재배포하거나 수정할 수 있습니다.

이 프로그램은 유용하게 사용될 수 있기를 바라며 배포되지만,
상품성이나 특정 목적에의 적합성에 대한 묵시적 보증을 포함한
어떠한 보증도 하지 않습니다. 자세한 내용은
GNU Affero General Public License를 참조하세요.

이 프로그램과 함께 GNU Affero General Public License 사본을 받았을 것입니다.
받지 못했다면 <https://www.gnu.org/licenses/>를 참조하세요.

**이 프로젝트에 기여함으로써, 귀하는 기여 내용을 동일한 라이선스로
공개하는 데 동의하는 것으로 간주됩니다.**


## 원본 레포지토리

이 프로젝트는 [p-e-w/heretic](https://github.com/p-e-w/heretic)의 포크입니다.
원본 레포지토리의 모든 업데이트는 정기적으로 이 포크에 동기화됩니다.

한국어 관련 문의사항은 이 레포지토리의 Issues를 이용해 주세요.
