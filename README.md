# freeplaneGPT
quick tool written in chatgpt for optimising my personal research mindmaps

In the end I asked this: based on the format of that file Write a python script which does the following using the openai library: Load a freeplane mindmap file referenced from a command line argument, and parse it. Read the OpenAI API key from the "api.key" file. Read the list of topics from the "topics.txt" file. Extract social meta tags from each URL found in the mindmap nodes and replace the corresponding node's TEXT attribute. If the website sends back an error then skip to the next url node Retrieve the first 2000 characters of each URL's content and send it to the ChatGPT API for summarization and a best guess at one of the topics from the list and a catagory called other, where there is no good fit. Write the 500-character summary back to a new child node under each corresponding URL node. Assign labels (topics) to the nodes based on ChatGPT's best guess and move the nodes to appropriate sections of the mindmap. Save the updated mindmap to a new file

This Python code performs the following tasks:

It imports the necessary modules for web scraping, natural language processing, and parsing XML files.

It defines a function get_social_meta_tags that takes a URL as input and returns social meta tags (such as Open Graph and Twitter tags) and title tags for that URL. The function uses the requests module to fetch the HTML content of the web page, and the BeautifulSoup module to parse the HTML and extract the desired tags.

It defines a function get_summary_and_category that takes an API key, a block of text, and a list of topic categories as input, and returns a summary of the text and a category for that text. The function uses the OpenAI API to generate the summary and suggest the category based on the provided topics.

It defines a function update_mindmap that takes a Freeplane mindmap file, an API key, and a list of topic categories as input, and updates the mindmap with summaries and categories for each node that contains a URL attribute. The function uses the lxml module to parse and manipulate the mindmap XML file, and calls the get_social_meta_tags and get_summary_and_category functions to get the necessary information for each node.

It defines a main function that takes the path to a Freeplane mindmap file as input, reads the API key and list of topics from separate files, loads and parses the mindmap file, updates the mindmap with summaries and categories using the update_mindmap function, saves the updated mindmap to a new file, and prints a message confirming the file was saved.

It uses the argparse module to parse the command-line arguments, and calls the main function with the path to the mindmap file as input.

In summary, this code is a tool for automatically generating summaries and categorizing web pages in a Freeplane mindmap file using natural language processing and web scraping techniques.


