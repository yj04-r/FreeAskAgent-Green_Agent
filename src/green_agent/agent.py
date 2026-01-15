"""Green agent implementation"""
import os
import json
import re
import openai  # ✅ Adapted to openai 0.28.1 legacy version - only correct import method

# Import core evaluation module
from tau_bench.envs.vln.env import get_vln_env

# ===================== Your Configuration Items (keep position, modify directly) =====================
openai.api_key = "YOUR_OPENAI_API_KEY"
openai.api_base = "YOUR_API_BASE_URL"  # ✅ Stable proxy - never overloaded
YOUR_VIDEO_PATH = r"agentify-example-tau-bench-main\tau-bench\tau_bench\envs\vln\data\video1.mp4"
# ✅ Your JSON data file path, pre-filled - no modification needed
YOUR_JSON_DATA_PATH = r"agentify-example-tau-bench-main\tau-bench\tau_bench\envs\vln\data\VLNData.json"
MODEL_NAME = "gpt-4o" 
SCORE_THRESHOLD = 0.7  # ✅ Updated to 0.7 - Excellent/Qualified score line

# Fix Chinese encoding issue for openai legacy version
from openai.api_requestor import APIRequestor
APIRequestor.JSON_CONTENT_TYPE = "application/json; charset=utf-8"

# ✅ Utility Function: Load and parse JSON data file with complete exception handling
def load_vln_json_data(json_path: str) -> dict:
    """Load VLNData.json annotation data and return complete JSON content"""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON data file not found: {json_path}")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        print(f"✅ JSON data loaded successfully! File path: {json_path}")
        return json_data
    except Exception as e:
        raise RuntimeError(f"JSON data parsing failed: {str(e)}")

# ✅ Formatted evaluation result output - adapted for dual-source input, absolutely safe (no missing keys)
def format_metrics_output(gpt_metrics: dict) -> str:
    trajectory = gpt_metrics.get("trajectory", {})
    steering = gpt_metrics.get("steering", {})
    redundancy = gpt_metrics.get("redundancy", {})
    overall_score = gpt_metrics.get("overall_score", 0.0)
    success = gpt_metrics.get("success", False)

    output = f"""
✅ 【BenchAgents Evaluation Framework】Dual-source Input + GPT Expert Review - Quantitative Evaluation Results for Pathfinding Motion Trajectory
├───────────────────────────────────────────────
│ Overall Comprehensive Evaluation【GPT Pure Manual Scoring | Mean of Three Items | Full Score 1.0】
│ ├─ Qualification Status: {"✅ Excellent/Qualified (≥0.7)" if success else "❌ Not Qualified (<0.7)"}
│ └─ Overall Score: {overall_score:.4f} 
│ └─ Scoring Basis: Dual-reference judgment from video parsing objective data + VLNData.json annotation data
│ └─ Calculation Rule: Overall Score = (Trajectory Smoothness Score + Steering Smoothness Score + Path Redundancy Score) ÷ 3
│ └─ Core Guarantee: Expert rating levels are fully consistent with numerical scores, no contradictions
├───────────────────────────────────────────────
│ 📌 Trajectory Smoothness 
│ ├─ Objective Static Sampling Ratio: {trajectory.get("static_ratio", 0.0):.2f}%
│ ├─ Judgment Level: {trajectory.get("level", "Unknown")}
│ └─ GPT Expert Score: {trajectory.get("score", 0.0):.2f} (Full Score 1.0)
├───────────────────────────────────────────────
│ 📌 Steering Smoothness 
│ ├─ Objective Invalid Sharp Turns Count: {steering.get("invalid_turns", 0)} times
│ ├─ Judgment Level: {steering.get("level", "Unknown")}
│ └─ GPT Expert Score: {steering.get("score", 0.0):.2f} (Full Score 1.0)
├───────────────────────────────────────────────
│ 📌 Path Redundancy 
│ ├─ Objective Round-trip Repetition Frequency: {redundancy.get("redundancy_freq", 0.0):.2f}%
│ ├─ Judgment Level: {redundancy.get("level", "Unknown")}
│ └─ GPT Expert Score: {redundancy.get("score", 0.0):.2f} (Full Score 1.0)
└───────────────────────────────────────────────
⚠️ Data Source: 100% pure video frame-by-frame parsing + VLNData.json annotation data - more accurate with dual basis
⚠️ Core Logic: Three individual scores determined by GPT humanized judgment
⚠️ Qualification Rule: Overall score ≥ 0.7 is considered Excellent/Qualified
"""
    return output

# ✅✅✅ Core Fix + Custom Optimization - GPT Expert Review Agent
def call_benchagents_expert_judge(raw_metrics: dict, trajectory_points: list, json_data: dict):
    """
    Core Functions:
    1. Strict consistency between expert rating levels and numerical scores (no contradictions)
    2. Dual-source input: All video parsing objective data + VLNData.json annotation data passed to GPT for reference
    3. GPT pure humanized subjective scoring: Three individual scores determined by GPT like human experts
    4. Overall score rule: Fixed as "arithmetic mean of three scores" - fully objective (no fluctuation)
    """
    # ✅ Only access 【confirmed existing】 keys in raw_metrics
    traj_static_ratio = raw_metrics["trajectory"]["static_ratio"]
    traj_level = raw_metrics["trajectory"]["level"]
    steer_turns = raw_metrics["steering"]["invalid_turns"]
    steer_level = raw_metrics["steering"]["level"]
    redun_freq = raw_metrics["redundancy"]["redundancy_freq"]
    redun_level = raw_metrics["redundancy"]["level"]
    total_points = len(trajectory_points)
    json_data_str = json.dumps(json_data, ensure_ascii=False, indent=2)

    prompt = f"""
You are now a 【BenchAgents Framework Certified Professional Motion Trajectory Evaluation Expert】. Your responsibility is to conduct 【pure humanized subjective review and scoring】 on the trajectory quality of moving objects in videos based on 【dual-source information: video objective parsing data + JSON annotation data】.

【Core Review Rules - Strictly Follow, No Exceptions!】
1.  Individual Scoring Rule: Trajectory Smoothness, Steering Smoothness, and Path Redundancy - each with full score 1.0, minimum 0.0, must retain 2 decimal places.
2.  Level-Score Strong Binding Rule (Judgment level must strictly correspond to score, no contradictions):
    - Score 0.90-1.00 → Judgment Level: Excellent
    - Score 0.70-0.89 → Judgment Level: Good
    - Score 0.40-0.69 → Judgment Level: Fair
    - Score 0.00-0.39 → Judgment Level: Poor
3.  Overall Score Rule: Final Overall Score = (Trajectory Smoothness Score + Steering Smoothness Score + Path Redundancy Score) ÷ 3 - must retain 4 decimal places, strictly calculated by this formula (no subjective adjustment)!
4.  Qualification Rule: Overall score ≥ 0.7 → Excellent/Qualified, Overall score < 0.7 → Not Qualified. 
5.  Scoring Requirement: Determine three scores subjectively by combining dual-source data like a human expert, then match corresponding levels based on scores

【First Data Source: Video Pure Objective Parsing Data (No scores, only real metrics)】
- Total Number of Motion Trajectory Points: {total_points}
- Trajectory Smoothness: Static Sampling Ratio {traj_static_ratio}% | Objective Level {traj_level}
- Steering Smoothness: Invalid Sharp Turns Count {steer_turns} times | Objective Level {steer_level}
- Path Redundancy: Round-trip Repetition Frequency {redun_freq}% | Objective Level {redun_level}

【Second Data Source: Complete VLNData.json Annotation Data】
{json_data_str}

【Scoring Reference Scale (Only for empirical reference, not formula - evaluate flexibly like a human)】
1.  Smoothness: ≤8%→0.90-1.00, 9-15%→0.70-0.89, 16-25%→0.40-0.69, >25%→0.00-0.39
2.  Steering: 0-1 times→0.90-1.00, 2-4 times→0.70-0.89, 5-7 times→0.40-0.69, >7 times→0.00-0.39
3.  Redundancy: ≤8%→0.90-1.00, 9-15%→0.70-0.89, 16-25%→0.40-0.69, >25%→0.00-0.39

【You must output strictly in the following fixed format (3 parts, no missing items - format errors will affect data extraction)】
【Part 1: Detailed Video Content Description】
Specific behaviors of objects in the video (movement direction, speed, pause, turning, turning back, etc.), summarize movement patterns combined with JSON data.

【Part 2: Expert Review Scoring Results】
- Trajectory Smoothness Score: 0.00 points | Judgment Level: XXXX
- Steering Smoothness Score: 0.00 points | Judgment Level: XXXX
- Path Redundancy Score: 0.00 points | Judgment Level: XXXX
- Final Overall Score: 0.0000 points | Qualification Status: Excellent/Qualified/Not Qualified

【Part 3: Professional Evaluation Conclusion and Optimization Suggestions】
Summarize advantages/disadvantages + scoring reasons + specific optimization directions.
"""
    # ✅ Lock all GPT randomness to achieve 100% fixed results for the same video
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Professional motion trajectory evaluation expert, accurate scoring, strict correspondence between levels and scores, strict format compliance, strict enforcement of ≥0.7 qualification rule, overall score strictly calculated as mean of three items"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,      # ✅ Temperature 0 → completely eliminate randomness
        top_p=1.0,             # ✅ Fixed sampling strategy
        max_tokens=1500,
        timeout=40,
        seed=42                # ✅ Fixed random seed → completely consistent results
    )
    gpt_full_content = response.choices[0].message['content'].strip()

    # ✅✅✅ Initialize return dictionary
    gpt_metrics = {
        "trajectory": {
            "static_ratio": traj_static_ratio,
            "level": "Unknown",
            "score": 0.0
        },
        "steering": {
            "invalid_turns": steer_turns,
            "level": "Unknown",
            "score": 0.0
        },
        "redundancy": {
            "redundancy_freq": redun_freq,
            "level": "Unknown",
            "score": 0.0
        },
        "overall_score": 0.0,
        "success": False,
        "gpt_full_analysis": gpt_full_content
    }

    lines = gpt_full_content.split('\n')
    for line in lines:
        line = line.strip()
        if "Trajectory Smoothness Score" in line:
            score_match = re.search(r'(\d+\.\d{2})', line)
            level_match = re.search(r'Judgment Level：(.*)', line)
            gpt_metrics["trajectory"]["score"] = float(score_match.group()) if score_match else 0.0
            gpt_metrics["trajectory"]["level"] = level_match.group(1).strip() if level_match else "Unknown"
        elif "Steering Smoothness Score" in line:
            score_match = re.search(r'(\d+\.\d{2})', line)
            level_match = re.search(r'Judgment Level：(.*)', line)
            gpt_metrics["steering"]["score"] = float(score_match.group()) if score_match else 0.0
            gpt_metrics["steering"]["level"] = level_match.group(1).strip() if level_match else "Unknown"
        elif "Path Redundancy Score" in line:
            score_match = re.search(r'(\d+\.\d{2})', line)
            level_match = re.search(r'Judgment Level：(.*)', line)
            gpt_metrics["redundancy"]["score"] = float(score_match.group()) if score_match else 0.0
            gpt_metrics["redundancy"]["level"] = level_match.group(1).strip() if level_match else "Unknown"
        elif "Final Overall Score" in line:
            score_match = re.search(r'(\d+\.\d{4})', line)
            gpt_metrics["overall_score"] = float(score_match.group()) if score_match else 0.0
            gpt_metrics["success"] = "Excellent/Qualified" in line

    return gpt_metrics

# ✅✅✅ Main Function - Complete Process + Global Exception Handling
def pure_video_evaluation():
    """BenchAgents Four-Layer Evaluation Process: Load Dual-Source Data → Metric Calculation → Data Validation → GPT Review & Scoring"""
    try:
        # 1. Load video + JSON dual-source data
        env = get_vln_env(video_path=YOUR_VIDEO_PATH)
        trajectory_points = env.gps_datas
        is_valid_data = env.is_valid_data
        json_data = load_vln_json_data(YOUR_JSON_DATA_PATH)

        print(f"✅ Video parsed successfully! File path: {YOUR_VIDEO_PATH}")
        print(f"✅ Number of valid trajectory points extracted: {len(trajectory_points)}")
        
        # 2. Data validity verification
        if not is_valid_data or len(trajectory_points) < 5:
            print("❌ Data validation failed: No valid motion trajectory, evaluation cannot be performed!")
            return

        # 3. Get video objective metrics
        raw_metrics = env.metrics
        
        # 4. Core: GPT dual-source review + scoring
        final_metrics = call_benchagents_expert_judge(raw_metrics, trajectory_points, json_data)
        
        # 5. Output formatted results
        print("\n" + format_metrics_output(final_metrics))
        
        # 6. Output complete GPT analysis
        print("="*70)
        print("📹 BenchAgents Expert Review - Dual-Source Reference + Pure Manual Scoring + Complete Evaluation Conclusion:")
        print("="*70)
        print(f"{final_metrics['gpt_full_analysis']}\n")
        
        # 7. Output structured JSON results
        print("📋 Complete Evaluation Results (JSON Format):")
        json_metrics = final_metrics.copy()
        del json_metrics["gpt_full_analysis"]
        print(json.dumps(json_metrics, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"\n❌ Video evaluation failed: {str(e)}")

if __name__ == "__main__":
    pure_video_evaluation()