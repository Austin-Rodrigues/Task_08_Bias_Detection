"""
create_visualizations.py
Generate publication-quality plots for the report.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np


def create_plots():
    """Generate all visualizations"""
    Path("analysis/figures").mkdir(parents=True, exist_ok=True)

    # Load data
    summary = pd.read_csv("analysis/summary_by_condition.csv")
    detailed = pd.read_csv("analysis/all_runs_scored.csv")

    print("Creating visualizations...\n")

    # Plot 1: Sentiment comparison by hypothesis
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    families = ["H1_framing", "H2_demo", "H3_priming"]
    titles = ["H1: Framing Effect", "H2: Demographic Bias", "H3: Priming Bias"]

    for idx, (family, title) in enumerate(zip(families, titles)):
        data = summary[summary.prompt_family == family]
        ax = axes[idx]

        x = range(len(data))
        bars = ax.bar(x, data.vader_mean, yerr=data.vader_std,
                      capsize=5, alpha=0.7, color=['#2ecc71', '#e74c3c', '#3498db'][:len(data)])
        ax.set_xticks(x)
        ax.set_xticklabels(data.condition, rotation=45, ha='right')
        ax.set_ylabel('VADER Sentiment Score', fontsize=10)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_ylim(-1, 1)
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5, linewidth=1)
        ax.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for i, (bar, val) in enumerate(zip(bars, data.vader_mean)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig('analysis/figures/sentiment_comparison.png',
                dpi=300, bbox_inches='tight')
    print("✓ Saved analysis/figures/sentiment_comparison.png")

    # Plot 2: Response length comparison
    fig, ax = plt.subplots(figsize=(10, 6))

    for family in summary.prompt_family.unique():
        data = summary[summary.prompt_family == family]
        ax.plot(data.condition, data.len_mean, marker='o', label=family,
                linewidth=2, markersize=8)

    ax.set_xlabel('Condition', fontsize=11)
    ax.set_ylabel('Average Response Length (characters)', fontsize=11)
    ax.set_title('Response Length by Condition',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('analysis/figures/length_comparison.png',
                dpi=300, bbox_inches='tight')
    print("✓ Saved analysis/figures/length_comparison.png")

    # Plot 3: Player mention heatmap
    fig, ax = plt.subplots(figsize=(10, 6))

    player_cols = [f'mentions_{p}' for p in ['A', 'B', 'C', 'D', 'E', 'F']]
    mention_data = detailed.groupby(['prompt_family', 'condition'])[
        player_cols].mean()

    im = ax.imshow(mention_data.values, cmap='YlOrRd', aspect='auto')

    ax.set_xticks(range(len(player_cols)))
    ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F'])
    ax.set_yticks(range(len(mention_data)))
    ax.set_yticklabels(
        [f"{idx[0]}\n{idx[1]}" for idx in mention_data.index], fontsize=8)

    ax.set_xlabel('Player', fontsize=11)
    ax.set_ylabel('Condition', fontsize=11)
    ax.set_title('Average Player Mentions by Condition',
                 fontsize=13, fontweight='bold')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Mentions', fontsize=10)

    # Add text annotations
    for i in range(len(mention_data)):
        for j in range(len(player_cols)):
            text = ax.text(j, i, f'{mention_data.values[i, j]:.1f}',
                           ha="center", va="center", color="black", fontsize=8)

    plt.tight_layout()
    plt.savefig('analysis/figures/player_mentions_heatmap.png',
                dpi=300, bbox_inches='tight')
    print("✓ Saved analysis/figures/player_mentions_heatmap.png")

    plt.close('all')
    print("\n✓ All visualizations created")


if __name__ == "__main__":
    create_plots()
