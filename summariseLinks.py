import argparse
import requests
from bs4 import BeautifulSoup
import openai
from lxml import etree

def get_social_meta_tags(url):
    # Request the web page
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        print(f"Error fetching URL: {url}")
        return ""

    # If the response is not successful, return an empty string
    if response.status_code != 200:
        print(f"Failed to fetch URL: {url}")
        return ""

    # Parse the response and find meta tags and title tags
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all(['meta', 'title'])

    # Filter the tags based on specific attributes
    social_tags = [str(tag) for tag in tags if tag.has_attr('property') or tag.has_attr('name')]
    return ' '.join(social_tags)

def get_summary_and_category(api_key, text, topics):
    # Set the API key for OpenAI
    openai.api_key = api_key

    # Send a request to the OpenAI API for summarization and topic suggestion
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Summarize the following text in 500 characters and suggest one of the following topics: {', '.join(topics)} or 'other'.\n\n{text}",
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the summary and category from the response
    summary_and_category = response.choices[0].text.strip()
    if '\n' not in summary_and_category:
        return summary_and_category, 'other'
    summary, category = summary_and_category.split('\n', 1)
    return summary.strip(), category.strip()

def update_mindmap(mindmap, api_key, topics):
    # Iterate through all nodes with a URL attribute
    for node in mindmap.xpath('//node'):
        if 'LINK' in node.attrib:
            url = node.attrib['LINK']
            print(f"Processing URL: {url}")

            # Get social meta tags for the URL and update the node
            social_meta_tags = get_social_meta_tags(url)
            if 'TEXT' in node.attrib:
                node.attrib['TEXT'] += ' ' + social_meta_tags

            # Get the summary and category for the URL content
            summary, category = get_summary_and_category(api_key, url[:2000], topics)
            print(f"Summary: {summary}")
            print(f"Category: {category}")

            # Add the summary as a new child node and update the category
            summary_node = etree.SubElement(node, 'node', TEXT=summary)
            node.attrib['POSITION'] = category

def main(mindmap_file):
    # Read the API key from the "api.key" file
    with open("api.key", "r") as api_key_file:
        api_key = api_key_file.read().strip()

    # Read the list of topics from the "topics.txt" file
    with open("topics.txt", "r") as topics_file:
        topics = [topic.strip() for topic in topics_file.readlines()]

    # Load and parse the mindmap file
    try:
        mindmap = etree.parse(mindmap_file)
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML file: {e}")
        return

    # Update the mindmap with summaries and categories
    update_mindmap(mindmap, api_key, topics)

    # Save the updated mindmap to a new file
    updated_mindmap_file = f"updated_{mindmap_file}"
    with open(updated_mindmap_file, "wb") as output_file:
        output_file.write(etree.tostring(mindmap, pretty_print=True))

    print(f"Updated mindmap saved as {updated_mindmap_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a Freeplane mindmap file.")
    parser.add_argument("mindmap_file", help="Path to the Freeplane mindmap file.")
    args = parser.parse_args()

    main(args.mindmap_file)

