# FreeAskAgent-Green_Agent

We propose a pure video-based motion trajectory evaluation module integrated with the BenchAgents framework, which realizes **dual-source reference (video parsing + VLNData.json annotation)** and **GPT-4o expert subjective scoring**, ensuring 100% fixed evaluation results for the same video and strict consistency between expert scoring levels and numerical scores.

## Core Features
Dual-source Input: GPT-4o references both video-parsed objective motion metrics and VLNData.json annotation data for comprehensive evaluation
Pure Subjective Scoring: No hard-coded formula calculation, scoring power is fully delegated to GPT-4o simulating human experts
(Excellent/Good/Fair/Poor) and numerical scores
Threshold Calibration: Comprehensive score ≥ 0.7 is defined as "Excellent" (pass)

## Setup

1. Clone the repository :
```bash
git clone https://github.com/yj04-r/FreeAskAgent-Green_Agent && cd ./agentify-example-tau-bench-main
```

2. Install required dependencies:
```bash
pip install openai==0.28.1 opencv-python numpy
pip install -e .  # Install tau_bench from source
```

3. Configure API keys and file paths in `agent.py`:
```python
# In agent.py, update the following configurations
openai.api_key = "YOUR_OPENAI_API_KEY"
openai.api_base = "YOUR_API_BASE_URL"  
YOUR_VIDEO_PATH = "PATH_TO_YOUR_VIDEO.mp4"
YOUR_JSON_DATA_PATH = "PATH_TO_VLNData.json"
```

## Run

### Basic Evaluation
Run the pure video trajectory evaluation with default settings:
```bash
python -m src.green_agent.agent
```

### Key Parameters Explanation
- `MODEL_NAME`: Default is "gpt-4o" (recommended for expert-level scoring)
- `SCORE_THRESHOLD`: Default is 0.7 (comprehensive score ≥ 0.7 = Excellent/Pass)
- `temperature=0`: Eliminates randomness in GPT responses
- `seed=42`: Fixes random seed to ensure deterministic results

## Evaluation Metrics

| Metric                | Calculation Logic                                                                 | Scoring Rule (GPT Reference)                          |
|-----------------------|-----------------------------------------------------------------------------------|-------------------------------------------------------|
| Trajectory Smoothness | Static sampling ratio from video frame parsing                                    | ≤8%→0.90-1.00, 9-15%→0.70-0.89, 16-25%→0.40-0.69, >25%→0.00-0.39 |
| Steering Smoothness   | Invalid sharp turn count calculated from trajectory points                        | 0-1→0.90-1.00, 2-4→0.70-0.89, 5-7→0.40-0.69, >7→0.00-0.39 |
| Path Redundancy       | Round-trip repetition frequency of motion trajectory                              | ≤8%→0.90-1.00, 9-15%→0.70-0.89, 16-25%→0.40-0.69, >25%→0.00-0.39 |
| Comprehensive Score   | Arithmetic mean of the three metrics (retained to 4 decimal places)               | ≥0.7→Excellent, <0.7→Not Pass                         |

## Output Example

```
✅ 【BenchAgents Evaluation Framework】Dual-source Input + GPT Expert Review - Quantitative Evaluation Results for Pathfinding Motion Trajectory
├───────────────────────────────────────────────
│ Overall Comprehensive Evaluation【GPT Pure Manual Scoring | Mean of Three Items | Full Score 1.0】
│ ├─ Qualification Status: ✅ Excellent/Qualified (≥0.7)
│ └─ Overall Score: 0.9667 
│ └─ Scoring Basis: Dual-reference judgment from video parsing objective data + VLNData.json annotation data
│ └─ Calculation Rule: Overall Score = (Trajectory Smoothness Score + Steering Smoothness Score + Path Redundancy Score) ÷ 3
│ └─ Core Guarantee: Expert rating levels are fully consistent with numerical scores, no contradictions
├───────────────────────────────────────────────
│ 📌 Trajectory Smoothness
│ ├─ Objective Static Sampling Ratio: 0.00%
│ ├─ Judgment Level: Unknown
│ └─ GPT Expert Score: 1.00 (Full Score 1.0)
├───────────────────────────────────────────────
│ 📌 Steering Smoothness
│ ├─ Objective Invalid Sharp Turns Count: 1 times
│ ├─ Judgment Level: Unknown
│ └─ GPT Expert Score: 0.90 (Full Score 1.0)
├───────────────────────────────────────────────
│ 📌 Path Redundancy
│ ├─ Objective Round-trip Repetition Frequency: 0.00%
│ ├─ Judgment Level: Unknown
│ └─ GPT Expert Score: 1.00 (Full Score 1.0)
└───────────────────────────────────────────────
⚠️ Data Source: 100% pure video frame-by-frame parsing + VLNData.json annotation data - more  accurate with dual basis
⚠️ Core Logic: Three individual scores determined by GPT humanized judgment
⚠️ Qualification Rule: Overall score ≥ 0.7 is considered Excellent/Qualified

======================================================================
📹 BenchAgents Expert Review - Dual-Source Reference + Pure Manual Scoring + Complete Evaluation Conclusion:
======================================================================
【Part 1: Detailed Video Content Description】
The video depicts an object moving through a cityscape, starting at position (6.21, 0.0, 5.26) and ending at (-7.51, 0.13, 64.08). The trajectory is characterized by a high degree of smoothness, with no static pauses and a consistent forward motion. The object makes one invalid sharp turn, indicating a minor deviation from the intended path. The path shows zero redundancy, as there are no round-trip repetitions. The movement is steady, with a clear direction towards the goal, "我和乔治 欧洲商品," located at (-8.16, 1.77, 64.07). The object navigates through various areas without notable landmarks, maintaining a consistent speed and direction. 

【Part 2: Expert Review Scoring Results】
- Trajectory Smoothness Score: 1.00 points | Judgment Level: Excellent
- Steering Smoothness Score: 0.90 points | Judgment Level: Excellent
- Path Redundancy Score: 1.00 points | Judgment Level: Excellent
- Final Overall Score: 0.9667 points | Qualification Status: Excellent/Qualified

【Part 3: Professional Evaluation Conclusion and Optimization Suggestions】
The trajectory demonstrates exceptional smoothness and minimal steering deviations, with only one sharp turn recorded. The path is highly efficient, with no redundancy, indicating optimal navigation towards the goal. The scoring reflects these strengths, with all aspects rated as excellent. To further optimize, consider refining the steering algorithm to eliminate the single sharp turn, ensuring even smoother transitions. Overall, the trajectory is highly effective and well-executed, meeting the criteria for qualification with an excellent status.     

📋 Complete Evaluation Results (JSON Format):
{
  "trajectory": {
    "static_ratio": 0.0,
    "level": "Unknown",
    "score": 1.0
  },
  "steering": {
    "invalid_turns": 1,
    "level": "Unknown",
    "score": 0.9
  },
  "redundancy": {
    "redundancy_freq": 0.0,
    "level": "Unknown",
    "score": 1.0
  },
  "overall_score": 0.9667,
  "success": true
}
```

## File Structure
| File               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `agent.py`         | Main entry: API configuration, GPT expert scoring logic, result formatting  |
| `env.py`           | Core module: Video parsing, trajectory extraction, objective metric calculation |
| `VLNData.json`     | Annotation data file for GPT reference (ensure path correctness)            |

## License
See ./LICENSE.

## Contact
Submit issues or pull requests for bug fixes or feature enhancements.

## Citation
If you use this evaluation module in your research, please cite the relevant BenchAgents framework paper and this work:
@inproceedings{
butt2025benchagents,
title={BenchAgents: Automated Benchmark Creation with Agent Interaction},
author={Natasha Butt and Varun Chandrasekaran and Neel Joshi and Besmira Nushi and Vidhisha Balachandran},
booktitle={ICLR 2025 Workshop on Navigating and Addressing Data Problems for Foundation Models},
year={2025},
url={https://openreview.net/forum?id=Xh6S3X3enu}
}
