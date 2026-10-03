"""Local dependency-free web demo for the recommendation pipeline.

The server accepts a form on localhost, runs the offline hybrid method and
renders grounded recommendations with official programme links.
"""

from __future__ import annotations

import html
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from .pipeline import recommend


FORM = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>SGGradMatch</title><style>
body{font:16px system-ui;max-width:920px;margin:40px auto;padding:0 20px;color:#172033}
h1{margin-bottom:4px} .muted{color:#5b6475} form{display:grid;grid-template-columns:1fr 1fr;gap:14px}
label{display:flex;flex-direction:column;gap:5px;font-weight:600} input,select{box-sizing:border-box;height:42px;padding:10px;border:1px solid #aeb6c4;border-radius:7px;font:inherit;background:#fff}
.wide{grid-column:1/-1}button{padding:11px 18px;background:#173b69;color:white;border:0;border-radius:7px;font-weight:700}
.card{border:1px solid #d9dee7;border-radius:10px;padding:18px;margin:16px 0}.score{float:right;font-weight:700}
a{color:#174f91}.warning{color:#8b4a00}code{background:#f2f4f7;padding:2px 5px;border-radius:4px}
</style></head><body><h1>SGGradMatch</h1><p class="muted">Grounded decision support for a curated set of Singapore master's programmes. It does not predict admission.</p>
<form method="post">
<label class="wide">Academic background<input name="academic_background" value="__ACADEMIC_BACKGROUND__" placeholder="e.g. business analytics" required></label>
<label class="wide">Career goal<input name="career_goal" value="__CAREER_GOAL__" placeholder="e.g. become a data scientist working on business problems" required></label>
<label class="wide">Interests separated by commas<input name="interests" value="__INTERESTS__" placeholder="e.g. machine learning, data science, business analytics"></label>
<label>Maximum tuition in SGD<input name="budget_sgd" type="number" value="__BUDGET_SGD__" placeholder="e.g. 65000"></label>
<label>Maximum duration in months<input name="max_duration_months" type="number" value="__MAX_DURATION_MONTHS__" placeholder="e.g. 18"></label>
<label>Study mode<select name="preferred_mode"><option value="full-time"__FULL_TIME_SELECTED__>Full-time</option><option value="part-time"__PART_TIME_SELECTED__>Part-time</option></select></label>
<label>Years of experience<input name="years_experience" type="number" step="0.5" value="__YEARS_EXPERIENCE__" placeholder="e.g. 2"></label>
<div class="wide"><button type="submit">Generate recommendations</button></div></form>{results}</body></html>"""


def render_page(values: dict[str, str] | None = None, results: str = "") -> str:
    """Render an empty form or preserve only the values the user submitted."""
    values = values or {}

    def escaped(name: str) -> str:
        return html.escape(str(values.get(name, "")), quote=True)

    preferred_mode = values.get("preferred_mode", "full-time")
    replacements = {
        "__ACADEMIC_BACKGROUND__": escaped("academic_background"),
        "__CAREER_GOAL__": escaped("career_goal"),
        "__INTERESTS__": escaped("interests"),
        "__BUDGET_SGD__": escaped("budget_sgd"),
        "__MAX_DURATION_MONTHS__": escaped("max_duration_months"),
        "__YEARS_EXPERIENCE__": escaped("years_experience"),
        "__FULL_TIME_SELECTED__": " selected" if preferred_mode == "full-time" else "",
        "__PART_TIME_SELECTED__": " selected" if preferred_mode == "part-time" else "",
    }
    page = FORM.replace("{results}", results)
    for token, replacement in replacements.items():
        page = page.replace(token, replacement)
    return page


def result_html(result: dict) -> str:
    """Escape and render a recommendation response as HTML fragments."""
    if result.get("status") != "ok":
        return f'<p class="warning">{html.escape(result.get("message", "Unable to recommend."))}</p>'
    blocks = [f'<h2>Recommendations</h2><p class="muted">{html.escape(result["message"])}</p>']
    for item in result["recommendations"]:
        reasons = "".join(f"<li>{html.escape(reason)}</li>" for reason in item["fit"])
        warnings = "".join(f"<li>{html.escape(note)}</li>" for note in item["trade_offs"])
        blocks.append(
            '<section class="card">'
            f'<span class="score">{item["score"]:.3f}</span>'
            f'<h3>{html.escape(item["programme_name"])}</h3>'
            f'<p>{html.escape(item["university"])}</p><h4>Why it fits</h4><ul>{reasons}</ul>'
            f'<h4>Checks</h4><ul class="warning">{warnings}</ul>'
            f'<p><a href="{html.escape(item["source_url"], quote=True)}" target="_blank">Official source</a> · verified {html.escape(item["last_verified_at"])}</p>'
            '</section>'
        )
    return "".join(blocks)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        self._send(render_page())

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        fields = parse_qs(self.rfile.read(length).decode("utf-8"))
        def value(name: str, default: str = "") -> str:
            return fields.get(name, [default])[0]
        profile = {
            "profile_id": "web-demo",
            "academic_background": value("academic_background"),
            "career_goal": value("career_goal"),
            "interests": [item.strip() for item in value("interests").split(",") if item.strip()],
            "budget_sgd": value("budget_sgd") or None,
            "preferred_mode": value("preferred_mode", "full-time"),
            "max_duration_months": value("max_duration_months") or None,
            "years_experience": value("years_experience", "0"),
        }
        try:
            result = recommend(profile, method="hybrid")
            page = render_page({name: value(name) for name in fields}, result_html(result))
        except Exception as exc:  # visible demo error, no hidden failure
            page = render_page(
                {name: value(name) for name in fields},
                f'<p class="warning">{html.escape(str(exc))}</p>',
            )
        self._send(page)

    def _send(self, page: str) -> None:
        body = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("SGGradMatch running at http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
