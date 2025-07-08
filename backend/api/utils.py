def format_table_for_ai(extracted_data):
    tables = extracted_data.get("tables", [])
    if not tables:
        return "No table data found."

    table = tables[0]

    formatted_sections = []
    current_section = None
    section_rows = []

    for row in table:
        stripped = [cell.strip() for cell in row]
        non_empty = [c for c in stripped if c]

        # Section header: exactly one non-empty cell
        if len(non_empty) == 1 and all(cell == "" or cell == non_empty[0] for cell in stripped):
            if current_section and section_rows:
                formatted_sections.append((current_section, section_rows))
                section_rows = []
            current_section = non_empty[0].title()
            continue

        # Skip empty rows
        if not non_empty:
            continue

        # Add normal data row
        section_rows.append(stripped)

    # Add final section
    if current_section and section_rows:
        formatted_sections.append((current_section, section_rows))

    # Prompt preamble
    lines = []
    lines.append("You are an experienced medical assistant.")
    lines.append("A patient has uploaded their blood report.")
    lines.append("Your job is to generate a health summary that is:")
    lines.append("• Clear and **easy to understand**, for someone with no medical background.")
    lines.append("• **Balanced** — not too technical, but not oversimplified.")
    lines.append("• Focused on **important values** or anything that might require attention.")
    lines.append("• Written in 3-6 short paragraphs.")
    lines.append("• Avoid lists unless necessary.")
    lines.append("• If everything looks normal, mention it but still explain a few key parameters briefly.")
    lines.append("• Avoid scary words or assumptions. Don’t over-diagnose.")
    lines.append("• Do **not** exceed 200 words.\n")

    lines.append("Here is the lab report in sections:\n")

    # Format each section as markdown
    for section, rows in formatted_sections:
        lines.append(f"## {section}")
        lines.append(" | ".join(rows[0]))  # header
        lines.append("-" * 50)
        for row in rows[1:]:
            lines.append(" | ".join(row))
        lines.append("")

    return "\n".join(lines)



import requests
import os

def call_deepseek_ai(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",  # or "deepseek-coder" if you're using that
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"DeepSeek failed: {response.status_code}\n{response.text}")
