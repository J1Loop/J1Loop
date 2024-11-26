import pathlib
from datetime import datetime as dt

import feedparser

ROOT = pathlib.Path(__file__).parent.resolve()
README_PATH = ROOT / "README.md"
FEED_URL = "https://1loop.dev/feed.xml"


def format_date(date_str: str) -> str:
    try:
        # Tue, 19 Nov 2024 00:00:00 GMT (RSS format)
        date = dt.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")

        # 19 Nov 2024
        return date.strftime("%d %b %Y")
    except ValueError:
        return date_str


def fetch_blog_entries(feed_url: str, max_posts: int = 5) -> list[dict[str, str]]:
    feed = feedparser.parse(feed_url)
    posts = []

    for entry in feed.entries[:max_posts]:
        formatted_date = format_date(entry.published)
        posts.append(
            {
                "title": entry.title,
                "description": entry.description,
                "link": entry.link,
                "published": formatted_date,
                "publish_order": dt.strptime(
                    entry.published, "%a, %d %b %Y %H:%M:%S %Z"
                ),
            }
        )

        posts.sort(key=lambda x: x["publish_order"], reverse=True)

    return posts


def update_readme(readme_path: pathlib.Path, posts: list[dict[str, str]]) -> None:

    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.readlines()

    start_marker = "<!-- BLOG-POSTS-START -->\n"
    end_marker = "<!-- BLOG-POSTS-END -->\n"

    try:
        start_idx = content.index(start_marker) + 1
        end_idx = content.index(end_marker)
    except ValueError:
        print("No se encontraron los marcadores en el README.")
        return

    new_section = ["| **Post Title** | **Post Description** | **Date Published** |\n"]
    new_section.append(
        "| -------------- | -------------------- | ------------------ |\n"
    )

    for post in posts:

        new_section.append(
            f"| [{post['title']}]({post['link']}) | {post['description']} | {post['published']} |\n"
        )

    content[start_idx:end_idx] = new_section

    with open(readme_path, "w", encoding="utf-8") as file:
        file.writelines(content)


def main():
    print("Fetching blog entries...")
    posts = fetch_blog_entries(FEED_URL, 5)

    print("Updating README...")
    update_readme(README_PATH, posts)

    print("README updated with latest blog posts successfully.")


if __name__ == "__main__":
    main()
