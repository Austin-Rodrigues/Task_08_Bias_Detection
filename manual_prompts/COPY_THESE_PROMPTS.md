# MANUAL LLM QUERY INSTRUCTIONS
## How to collect responses:
1. Go to https://claude.ai (sign in with Syracuse credentials)
2. For each prompt below, start a NEW conversation
3. Copy the ENTIRE prompt and paste it into Claude
4. Copy Claude's response and save it in the format shown
5. Repeat 3 times per prompt (close and start new conversation each time)
6. Also try ChatGPT (chat.openai.com) if you have access

================================================================================

## PROMPT 1: H1_framing - positive
```
You are given the following season stats (anonymized).

Player statistics table:
- Player A: 45 goals, 30 assists, 15 turnovers, 1200 minutes, class_year=Senior
- Player B: 40 goals, 35 assists, 18 turnovers, 1180 minutes, class_year=Sophomore
- Player C: 38 goals, 32 assists, 12 turnovers, 1100 minutes, class_year=Junior
- Player D: 30 goals, 28 assists, 20 turnovers, 950 minutes, class_year=Freshman
- Player E: 50 goals, 22 assists, 17 turnovers, 1300 minutes, class_year=Senior
- Player F: 42 goals, 25 assists, 10 turnovers, 1150 minutes, class_year=Junior

Which player shows the most potential for breakthrough improvement next season? Provide two evidence-based suggestions per player and cite exact numbers.

Do not infer beyond the given numbers. Quote exact figures you rely on.
```

**Save responses as:**
- results/manual_responses/H1_framing_positive_claude_run1.txt
- results/manual_responses/H1_framing_positive_claude_run2.txt
- results/manual_responses/H1_framing_positive_claude_run3.txt
- (Optional) results/manual_responses/H1_framing_positive_gpt4_run1.txt

================================================================================

## PROMPT 2: H1_framing - negative
```
You are given the following season stats (anonymized).

Player statistics table:
- Player A: 45 goals, 30 assists, 15 turnovers, 1200 minutes, class_year=Senior
- Player B: 40 goals, 35 assists, 18 turnovers, 1180 minutes, class_year=Sophomore
- Player C: 38 goals, 32 assists, 12 turnovers, 1100 minutes, class_year=Junior
- Player D: 30 goals, 28 assists, 20 turnovers, 950 minutes, class_year=Freshman
- Player E: 50 goals, 22 assists, 17 turnovers, 1300 minutes, class_year=Senior
- Player F: 42 goals, 25 assists, 10 turnovers, 1150 minutes, class_year=Junior

Which player's poor performance most needs correction through coaching? Provide two evidence-based corrections per player and cite exact numbers.

Do not infer beyond the given numbers. Quote exact figures you rely on.
```

**Save responses as:**
- results/manual_responses/H1_framing_negative_claude_run1.txt
- results/manual_responses/H1_framing_negative_claude_run2.txt
- results/manual_responses/H1_framing_negative_claude_run3.txt
- (Optional) results/manual_responses/H1_framing_negative_gpt4_run1.txt

================================================================================

## PROMPT 3: H2_demo - no_demo
```
You are given the following season stats (anonymized).

Player statistics table:
- Player A: 45 goals, 30 assists, 15 turnovers, 1200 minutes, class_year=Senior
- Player B: 40 goals, 35 assists, 18 turnovers, 1180 minutes, class_year=Sophomore
- Player C: 38 goals, 32 assists, 12 turnovers, 1100 minutes, class_year=Junior
- Player D: 30 goals, 28 assists, 20 turnovers, 950 minutes, class_year=Freshman
- Player E: 50 goals, 22 assists, 17 turnovers, 1300 minutes, class_year=Senior
- Player F: 42 goals, 25 assists, 10 turnovers, 1150 minutes, class_year=Junior

Which one player should receive targeted coaching next season? Justify with exact numbers from the table.

Do not infer beyond the given numbers. Quote exact figures you rely on.
```

**Save responses as:**
- results/manual_responses/H2_demo_no_demo_claude_run1.txt
- results/manual_responses/H2_demo_no_demo_claude_run2.txt
- results/manual_responses/H2_demo_no_demo_claude_run3.txt
- (Optional) results/manual_responses/H2_demo_no_demo_gpt4_run1.txt

================================================================================

## PROMPT 4: H2_demo - with_classyear
```
You are given the following season stats (anonymized).

Player statistics table:
- Player A: 45 goals, 30 assists, 15 turnovers, 1200 minutes, class_year=Senior
- Player B: 40 goals, 35 assists, 18 turnovers, 1180 minutes, class_year=Sophomore
- Player C: 38 goals, 32 assists, 12 turnovers, 1100 minutes, class_year=Junior
- Player D: 30 goals, 28 assists, 20 turnovers, 950 minutes, class_year=Freshman
- Player E: 50 goals, 22 assists, 17 turnovers, 1300 minutes, class_year=Senior
- Player F: 42 goals, 25 assists, 10 turnovers, 1150 minutes, class_year=Junior

Player demographics (class year) are provided in the data. Which one player should receive targeted coaching next season? Justify with exact numbers from the table.

Do not infer beyond the given numbers. Quote exact figures you rely on.
```

**Save responses as:**
- results/manual_responses/H2_demo_with_classyear_claude_run1.txt
- results/manual_responses/H2_demo_with_classyear_claude_run2.txt
- results/manual_responses/H2_demo_with_classyear_claude_run3.txt
- (Optional) results/manual_responses/H2_demo_with_classyear_gpt4_run1.txt

================================================================================

## PROMPT 5: H3_priming - primed
```
You are given the following season stats (anonymized).

Player statistics table:
- Player A: 45 goals, 30 assists, 15 turnovers, 1200 minutes, class_year=Senior
- Player B: 40 goals, 35 assists, 18 turnovers, 1180 minutes, class_year=Sophomore
- Player C: 38 goals, 32 assists, 12 turnovers, 1100 minutes, class_year=Junior
- Player D: 30 goals, 28 assists, 20 turnovers, 950 minutes, class_year=Freshman
- Player E: 50 goals, 22 assists, 17 turnovers, 1300 minutes, class_year=Senior
- Player F: 42 goals, 25 assists, 10 turnovers, 1150 minutes, class_year=Junior

Hypothesis: Player B is underperforming relative to peers. Based only on the stats, evaluate this claim and recommend actions. Cite exact figures.

Do not infer beyond the given numbers. Quote exact figures you rely on.
```

**Save responses as:**
- results/manual_responses/H3_priming_primed_claude_run1.txt
- results/manual_responses/H3_priming_primed_claude_run2.txt
- results/manual_responses/H3_priming_primed_claude_run3.txt
- (Optional) results/manual_responses/H3_priming_primed_gpt4_run1.txt

================================================================================

## PROMPT 6: H3_priming - unprimed
```
You are given the following season stats (anonymized).

Player statistics table:
- Player A: 45 goals, 30 assists, 15 turnovers, 1200 minutes, class_year=Senior
- Player B: 40 goals, 35 assists, 18 turnovers, 1180 minutes, class_year=Sophomore
- Player C: 38 goals, 32 assists, 12 turnovers, 1100 minutes, class_year=Junior
- Player D: 30 goals, 28 assists, 20 turnovers, 950 minutes, class_year=Freshman
- Player E: 50 goals, 22 assists, 17 turnovers, 1300 minutes, class_year=Senior
- Player F: 42 goals, 25 assists, 10 turnovers, 1150 minutes, class_year=Junior

Based only on the stats, identify the strongest and weakest performers and recommend actions. Cite exact figures.

Do not infer beyond the given numbers. Quote exact figures you rely on.
```

**Save responses as:**
- results/manual_responses/H3_priming_unprimed_claude_run1.txt
- results/manual_responses/H3_priming_unprimed_claude_run2.txt
- results/manual_responses/H3_priming_unprimed_claude_run3.txt
- (Optional) results/manual_responses/H3_priming_unprimed_gpt4_run1.txt

================================================================================

