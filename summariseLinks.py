import argparse
import requests
from bs4 import BeautifulSoup
import openai
from lxml import etree

def get_social_meta_tags(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        return ""

    if response.status_code != 200:
        return ""

    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all(['meta', 'title'])

    social_tags = [str(tag) for tag in tags if tag.has_attr('property') or tag.has_attr('name')]
    return ' '.join(social_tags)

def get_summary_and_category(api_key, text, topics):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Summarize the following text in 500 characters and suggest one of the following topics: {', '.join(topics)} or 'other'.\n\n{text}",
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary_and_category = response.choices[0].text.strip()
    if '\n' not in summary_and_category:
        return summary_and_category, 'other'
    summary, category = summary_and_category.split('\n', 1)
    return summary.strip(), category.strip()

def update_mindmap(mindmap, api_key, topics):
    for node in mindmap.xpath('//node'):
        if 'LINK' in node.attrib:
            url = node.attrib['LINK']
            social_meta_tags = get_social_meta_tags(url)
            if 'TEXT' in node.attrib:
                node.attrib['TEXT'] += ' ' + social_meta_tags

            summary, category = get_summary_and_category(api_key, url[:2000], topics)
            summary_node = etree.SubElement(node, 'node', TEXT=summary)
            node.attrib['POSITION'] = category

def main(mindmap_file):
    with open("api.key", "r") as api_key_file:
        api_key = api_key_file.read().strip()

    with open("topics.txt", "r") as topics_file:
        topics = [topic.strip() for topic in topics_file.readlines()]

    try:
        mindmap = etree.parse(mindmap_file)
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML file: {e}")
        return

    update_mindmap(mindmap, api_key, topics)

    updated_mindmap_file = f"updated_{mindmap_file}"
    with open(updated_mindmap_file, "wb") as updated_file:
        updated_file.write(etree.tostring(mindmap, pretty_print=True, encoding="utf-8", xml_declaration=True))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a Freeplane mindmap file.")
    parser.add_argument("mindmap_file", type=str, help="Path to the Freeplane mindmap file")
    args = parser.parse_args()
    main(args.mindmap_file)
