#!/usr/bin/env python3
"""Create the backlog in your team repository with the GitHub CLI.

Usage (inside the team repo, after `gh auth login`):
    python create_issues.py issues.csv --milestone "PY-W2" --dry-run
    python create_issues.py issues.csv --milestone "PY-W2"
"""
import argparse
import csv
import subprocess

def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv_file")
    p.add_argument("--milestone", default=None)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    with open(args.csv_file, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("CSV file is empty.")
        return

    # 1. Safely extract and create labels
    labels = set()
    for r in rows:
        if r.get("labels"):
            for lab in r["labels"].split(","):
                if lab.strip():
                    labels.add(lab.strip())
        # Support Lab 2 format: dynamically add size labels if column exists
        if r.get("size"):
            labels.add(f"size:{r['size'].strip()}")

    for lab in sorted(labels):
        cmd = ["gh", "label", "create", lab, "--force"]
        print(" ".join(cmd)) if args.dry_run else subprocess.run(cmd, check=False)

    # 2. Create issues
    for r in rows:
        body = r['body']
        
        # Support Lab 2 format: Append component and size only if they exist in CSV
        if r.get("component") and r.get("size"):
            body += f"\n\n**Component:** {r['component']}\n**Size:** {r['size']}\n\n## Definition of Done\nSee DEFINITION_OF_DONE.md"
        
        cmd = ["gh", "issue", "create", "--title", r["title"], "--body", body]
        
        # Handle labels dynamically
        issue_labels = []
        if r.get("labels"):
            issue_labels.extend([l.strip() for l in r["labels"].split(",") if l.strip()])
        if r.get("size"):
            issue_labels.append(f"size:{r['size'].strip()}")
            
        if issue_labels:
            cmd += ["--label", ",".join(issue_labels)]
            
        # Handle assignee dynamically (Crucial for Python Bootcamp)
        if r.get("assignee"):
            for a in r["assignee"].split(","):
                if a.strip():
                    cmd += ["--assignee", a.strip()]
            
        if args.milestone:
            cmd += ["--milestone", args.milestone]
            
        print(" ".join(cmd[:4]) + " ...") if args.dry_run else subprocess.run(cmd, check=True)

    print(f"{len(rows)} issues {'would be ' if args.dry_run else ''}created.")

if __name__ == "__main__":
    main()