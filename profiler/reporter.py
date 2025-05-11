import os
import pandas as pd
from datetime import datetime

def generate_markdown_report(violations, score_summary, filepath = "..\\report\\data_quality_report.md"):
    """
    Create a Markdown report showing all validation issues and final score.

    Args:
        violations (List[Dict]): Combined list of all validation issues.
        score_summary (Dict): Output of score_violations().
        filepath (str): Output path for the markdown report.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# 🧪 Data Quality Report\n")
        f.write(f"Generated on: {datetime.now().isoformat()}\n\n")
        f.write(f"Threshold: {score_summary['threshold']}\n\n")
        f.write(f"**Total Issues:** {score_summary['issues_count']}\n\n")
        f.write(f"**Severity Points:** {score_summary['total_points']}\n\n")
        f.write(f"**Status:** {score_summary['status']}\n\n")
        f.write("---\n\n")

        if not violations:
            f.write("✅ No issues found.\n")
        else:
            for v in violations:
                f.write(f"### ❌ {v.get('rule') or v.get('alert')} — {v.get('field', 'N/A')}\n")
                f.write(f"- **Error**: {v.get('error')}\n")
                f.write(f"- **Severity**: {v.get('severity')} ({v.get('severity_points')})\n")
                if "row" in v:
                    f.write(f"- **Row**: {v['row']}\n")
                if "actual_value" in v:
                    f.write(f"- **Actual Value**: `{v['actual_value']}`\n")
                f.write(f"- **Timestamp**: {v.get('timestamp', 'N/A')}\n")
                f.write("\n---\n\n")
                
def generate_csv_report(violations, filepath="..\\report\\data_quality_report.csv"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if violations:
        df = pd.DataFrame(violations)
        df.to_csv(filepath, index=False, encoding="utf-8")


def generate_html_report(violations, score_summary, alerts, filepath="..\\report\\data_quality_report.html"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    html = f"""
    <html>
    <head><meta charset='utf-8'><title>Data Quality Report</title></head>
    <body>
    <h1>🧪 Data Quality Report</h1>
    <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>
    <p><strong>Total Issues:</strong> {score_summary['issues_count']}</p>
    <p><strong>Threshold:</strong> {score_summary['threshold']}</p>
    <p><strong>Severity Points:</strong> {score_summary['total_points']}</p>
    <p><strong>Status:</strong> {score_summary['status']}</p>
    <hr>
    """

    if not violations:
        html += "<p>✅ No issues found.</p>"
    else:
        for v in violations:
            html += f"<h3>❌ {v.get('rule')} — {v.get('field', 'N/A')}</h3>"
            html += "<ul>"
            html += f"<li><strong>Error:</strong> {v.get('error')}</li>"
            html += f"<li><strong>Severity:</strong> {v.get('severity')}" 
            html += f"<li><strong>Severity points:</strong> {v.get('severity_points')}</li>"
            if "row" in v:
                html += f"<li><strong>Row:</strong> {v['row']}</li>"
            if "actual_value" in v:
                html += f"<li><strong>Actual Value:</strong> {v['actual_value']}</li>"
            html += f"<li><strong>Timestamp:</strong> {v.get('timestamp', 'N/A')}</li>"
            html += "</ul><hr>"

    if not alerts:
        html += "<p>✅ No issues found.</p>"
    else:
        for a in alerts:
            html += f"<h3>❗️ {a.get('alert')} — {a.get('field', 'N/A')}</h3>"
            html += "<ul>"
            html += f"<li><strong>Alert:</strong> {a.get('alert')}</li>"
            html += f"<li><strong>Severity:</strong> {a.get('severity')}"
            if "threshold" in a:
                html += f"<li><strong>Threshold:</strong> {a['threshold']}</li>"
            if "tags" in a:
                html += f"<li><strong>Tags:</strong> {a['tags']}</li>" 

            html += f"<li><strong>Timestamp:</strong> {a.get('timestamp', 'N/A')}</li>"
            html += "</ul><hr>"

    html += "</body></html>"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
