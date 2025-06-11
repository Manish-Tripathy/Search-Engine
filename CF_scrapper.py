import requests


def save_problems_attributes():
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        return

    data = response.json()
    if data.get("status") != "OK":
        print(f"API error: {data.get('comment', 'Unknown error')}")
        return

    problems = data["result"]["problems"]

    contestIds = []
    indices = []
    names = []
    ratings = []
    all_tags = set()

    for p in problems:
        contestIds.append(str(p.get("contestId", "N/A")))
        indices.append(p.get("index", "N/A"))
        names.append(p.get("name", "N/A"))
        ratings.append(str(p.get("rating", "N/A")))
        # tags = [tag.strip() for tag in p.get("tags", [])]
        # all_tags.update(tags)

    # Write individual attributes (one value per problem)
    with open("CF_contestId.txt", "w") as f:
        f.write("\n".join(contestIds))
    with open("CF_index.txt", "w") as f:
        f.write("\n".join(indices))
    with open("CF_name.txt", "w") as f:
        f.write("\n".join(names))
    with open("CF_rating.txt", "w") as f:
        f.write("\n".join(ratings))


    with open("CF_problem_tags.txt", "w") as f:
        for p in problems:
            contest_id = p.get("contestId", "N/A")
            index = p.get("index", "N/A")
            tags = p.get("tags", [])
            tags_line = ", ".join(tags)
            f.write(f"{tags_line}\n")

    print(f"Saved {len(problems)} problems attributes and {len(all_tags)} unique tags.")


save_problems_attributes()
