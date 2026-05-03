import re
from difflib import SequenceMatcher


def fuzzy_match(a, b):
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


def brand_exists(response, brand):
    response_lower = response.lower()

    # direct match
    if brand.lower() in response_lower:
        return True

    # fuzzy word match
    words = response_lower.split()

    for i in range(len(words)):
        chunk = " ".join(words[i:i+3])

        if fuzzy_match(chunk, brand) > 0.75:
            return True

    return False


def analyze_responses(ai_responses, your_brand, competitors):
    all_brands = [your_brand] + competitors
    analysis = {}

    for brand in all_brands:
        brand_data = {
            "mentioned_by": [],
            "positions": {},
            "snippets": {},
            "mention_count": 0
        }

        for ai_name, response in ai_responses.items():

            if "Error" in response:
                continue

            if brand_exists(response, brand):
                brand_data["mentioned_by"].append(ai_name)
                brand_data["mention_count"] += 1

                pos = response.lower().find(
                    brand.lower().split()[0]
                )

                if pos == -1:
                    pos = len(response) // 2

                relative_pos = pos / len(response)

                if relative_pos < 0.33:
                    rank = "Top"
                elif relative_pos < 0.66:
                    rank = "Middle"
                else:
                    rank = "Bottom"

                brand_data["positions"][ai_name] = rank

                start = max(0, pos - 50)
                end = min(len(response), pos + 150)

                snippet = response[start:end].replace("\n", " ")

                brand_data["snippets"][ai_name] = snippet

        analysis[brand] = brand_data

    return analysis


def calculate_scores(analysis, ai_responses):
    valid_ais = [
        ai for ai, response in ai_responses.items()
        if "Error" not in response
    ]

    num_ais = len(valid_ais)

    if num_ais == 0:
        return {
            brand: 0
            for brand in analysis
        }

    scores = {}

    for brand, data in analysis.items():
        coverage = len(data["mentioned_by"]) / num_ais
        coverage_score = coverage * 60

        position_map = {
            "Top": 40,
            "Middle": 25,
            "Bottom": 10
        }

        position_score = 0

        if data["positions"]:
            position_score = sum(
                position_map[pos]
                for pos in data["positions"].values()
            ) / len(data["positions"])

        total = round(
            coverage_score + position_score
        )

        scores[brand] = min(total, 100)

    return scores


def generate_insights(analysis, scores, your_brand, ai_responses):
    insights = []

    your_score = scores.get(your_brand, 0)
    your_mentions = analysis[your_brand]["mentioned_by"]

    if not your_mentions:
        insights.append(
            f"🔴 {your_brand} wasn't mentioned by any AI engine."
        )

    elif len(your_mentions) < 3:
        insights.append(
            f"🟡 {your_brand} appears in only {len(your_mentions)} AI engines."
        )

    else:
        insights.append(
            f"🟢 Strong AI visibility across all engines."
        )

    top_competitors = [
        brand
        for brand, score in scores.items()
        if brand != your_brand and score > your_score
    ]

    if top_competitors:
        insights.append(
            f"⚠️ Competitors beating you: {', '.join(top_competitors)}"
        )

    if your_score < 40:
        insights.append(
            "🚀 Improve AI visibility with reviews, blogs, citations, Reddit mentions."
        )

    return insights