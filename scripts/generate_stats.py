import os
import sys
import json
import urllib.request
import subprocess

def get_token():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        try:
            token = subprocess.check_output(["gh", "auth", "token"]).decode("utf-8").strip()
        except Exception:
            pass
    return token

def fetch_graphql(token, query):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "danielxxomg-stats-generator",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def generate_stats_svg(data, output_path):
    user = data["data"]["user"]
    commits = user["contributionsCollection"]["totalCommitContributions"]
    restricted = user["contributionsCollection"]["restrictedContributionsCount"]
    total_commits = commits + restricted
    prs = user["pullRequests"]["totalCount"]
    issues = user["issues"]["totalCount"]
    contributed = user["repositoriesContributedTo"]["totalCount"]
    
    # Calculate stars across repositories
    stars = sum(repo["stargazerCount"] for repo in user["repositories"]["nodes"])

    svg = f"""<svg width="450" height="200" viewBox="0 0 450 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #FFA500; }}
    .stat-label {{ font: 400 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #94a3b8; }}
    .stat-value {{ font: 700 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #f8fafc; }}
    .icon {{ fill: #ff6b6b; }}
    .border {{ stroke: #334155; stroke-width: 1px; }}
    .bg {{ fill: #0f172a; }}
    .badge {{ font: 600 11px 'Segoe UI', Ubuntu, Sans-Serif; fill: #34d399; }}
  </style>
  <rect class="bg border" width="448" height="198" x="1" y="1" rx="10" />
  
  <!-- Header -->
  <text x="25" y="38" class="header">GitHub Overview</text>
  <rect x="345" y="22" width="80" height="22" rx="11" fill="#1e293b" stroke="#334155" />
  <circle cx="357" cy="33" r="4" fill="#34d399" />
  <text x="367" y="37" class="badge">ACTIVE</text>

  <!-- Items -->
  <g transform="translate(25, 65)">
    <!-- Total Commits -->
    <g transform="translate(0, 0)">
      <path class="icon" d="M10.5 0a5 5 0 0 0-4.9 4H1a1 1 0 0 0 0 2h4.6a5 5 0 0 0 9.8 0H20a1 1 0 1 0 0-2h-4.6A5 5 0 0 0 10.5 0zm0 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4z" transform="scale(0.8)"/>
      <text x="24" y="12" class="stat-label">Total Commits (Year):</text>
      <text x="220" y="12" class="stat-value">{total_commits:,}</text>
    </g>

    <!-- Pull Requests -->
    <g transform="translate(0, 28)">
      <path class="icon" d="M7 1a3 3 0 0 0-3 3c0 1.3.8 2.4 2 2.8v4.4c-1.2.4-2 1.5-2 2.8a3 3 0 0 0 6 0c0-1.3-.8-2.4-2-2.8V6.8c.6-.2 1.2-.6 1.6-1.1L12 8.1V11c-.6.3-1 .9-1 1.7a2 2 0 1 0 4 0c0-.8-.4-1.4-1-1.7V7.5L11.5 5c.3-.5.5-1.2.5-2a3 3 0 0 0-3-3H7z" transform="scale(0.8)"/>
      <text x="24" y="12" class="stat-label">Pull Requests:</text>
      <text x="220" y="12" class="stat-value">{prs:,}</text>
    </g>

    <!-- Issues -->
    <g transform="translate(0, 56)">
      <path class="icon" d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm0 12a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm1-5.5a1 1 0 1 1-2 0v-3a1 1 0 1 1 2 0v3z" transform="scale(0.8)"/>
      <text x="24" y="12" class="stat-label">Issues Opened:</text>
      <text x="220" y="12" class="stat-value">{issues:,}</text>
    </g>

    <!-- Contributed To -->
    <g transform="translate(0, 84)">
      <path class="icon" d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5v-9zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8V1.5z" transform="scale(0.8)"/>
      <text x="24" y="12" class="stat-label">Contributed Repositories:</text>
      <text x="220" y="12" class="stat-value">{contributed:,}</text>
    </g>

    <!-- Total Stars -->
    <g transform="translate(0, 112)">
      <path class="icon" d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25z" transform="scale(0.8)"/>
      <text x="24" y="12" class="stat-label">Total Stars Earned:</text>
      <text x="220" y="12" class="stat-value">{stars:,}</text>
    </g>
  </g>
</svg>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path}")

def generate_languages_svg(data, output_path):
    user = data["data"]["user"]
    lang_totals = {}
    lang_colors = {}
    
    EXCLUDED_LANGS = {"HTML", "CSS", "SCSS", "Less", "Markdown", "Jupyter Notebook"}
    
    for repo in user["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name in EXCLUDED_LANGS:
                continue
            color = edge["node"]["color"] or "#64748b"
            size = edge["size"]
            lang_totals[name] = lang_totals.get(name, 0) + size
            lang_colors[name] = color

    total_bytes = sum(lang_totals.values())
    sorted_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:5]

    items_svg = []
    y_offset = 65
    for name, size in sorted_langs:
        pct = (size / total_bytes) * 100 if total_bytes > 0 else 0
        color = lang_colors.get(name, "#38bdf8")
        bar_width = int((pct / 100) * 180)
        items_svg.append(f"""
    <g transform="translate(0, {y_offset - 65})">
      <circle cx="6" cy="7" r="5" fill="{color}" />
      <text x="20" y="11" class="lang-name">{name}</text>
      <rect x="180" y="4" width="180" height="8" rx="4" fill="#1e293b" />
      <rect x="180" y="4" width="{max(bar_width, 6)}" height="8" rx="4" fill="{color}" />
      <text x="375" y="11" class="lang-pct">{pct:.1f}%</text>
    </g>""")
        y_offset += 26

    svg = f"""<svg width="450" height="200" viewBox="0 0 450 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #FFA500; }}
    .lang-name {{ font: 500 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #f8fafc; }}
    .lang-pct {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #94a3b8; }}
    .border {{ stroke: #334155; stroke-width: 1px; }}
    .bg {{ fill: #0f172a; }}
  </style>
  <rect class="bg border" width="448" height="198" x="1" y="1" rx="10" />
  <text x="25" y="38" class="header">Top Languages</text>
  <g transform="translate(25, 65)">
    {"".join(items_svg)}
  </g>
</svg>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path}")

def main():
    token = get_token()
    if not token:
        print("Error: No GITHUB_TOKEN or gh CLI token available.", file=sys.stderr)
        sys.exit(1)
        
    query = """
    query {
      user(login: "danielxxomg") {
        name
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
        }
        repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
          totalCount
        }
        pullRequests(first: 1) {
          totalCount
        }
        issues(first: 1) {
          totalCount
        }
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
          totalCount
          nodes {
            name
            stargazerCount
            languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node {
                  name
                  color
                }
              }
            }
          }
        }
      }
    }
    """
    data = fetch_graphql(token, query)
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    os.makedirs(output_dir, exist_ok=True)
    generate_stats_svg(data, os.path.join(output_dir, "github-stats.svg"))
    generate_languages_svg(data, os.path.join(output_dir, "top-langs.svg"))

if __name__ == "__main__":
    main()
