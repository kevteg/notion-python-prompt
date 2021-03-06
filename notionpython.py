from notion_client import Client
import logging


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


class NotionPython:

    prompt = ">>>"

    prompt_child = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": prompt,
                    },
                },
            ],
            "color": "green",
        },
    }

    def __init__(self, token, page_id):
        """
        token: token to access the integration
        page_id: page to be used as the python 'interpreter'
        """
        self.notion = Client(auth=token)
        self.page_id = page_id

    def clean_page(self):
        logging.info("Removing entries")
        children = self.page_children()
        for child in children:
            if child.get("type") == "paragraph":
                self.notion.blocks.delete(block_id=child["id"])
        self.add_prompt()
        logging.info("Page cleaned")

    def page_children(self):
        # a page is a block in notion
        children_object = self.notion.blocks.children.list(block_id=self.page_id)
        children = children_object.get("results", [])
        return children

    def get_code(self, children):
        """iterates over the existing children of the page
        and returns the text that can be run as code
        """
        children = self.page_children()
        code = None
        for child in reversed(children):
            if child.get("type") == "paragraph":
                content = ""
                paragraph = child.get("paragraph")
                text = paragraph.get("text", [])
                if text:
                    text = text[0]
                    content = text.get("plain_text", "")
                if content.startswith(self.prompt):
                    code = content.strip(self.prompt)
                    # Replacing the most common unicode quotation marks
                    code = code.replace(u"\u201C", "'")
                    code = code.replace(u"\u201D", "'")
                    break
        return code

    def eval_code(self):
        children = self.page_children()
        code = self.get_code(children)
        try:
            logging.info("Last line found on notion: ")
            logging.info(code)
            if code:
                result = str(eval(code))
                result = result.replace("\n", "")
                logging.info("Sending result back to notion page")
                logging.info("Result:")
                logging.info(result)
                self.add_result(result)
            else:
                logging.info("Nothing to add")
        except Exception as e:
            logging.info("Error running code, check it out!")
            logging.info(e)

    def add_result(self, result):
        """appends the result and the prompt"""
        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": result,
                            },
                        },
                    ],
                    "color": "green",
                },
            },
            self.prompt_child,
        ]

        return self.__add_children(children)

    def add_prompt(self):
        """appends the prompt"""
        children = [self.prompt_child]

        return self.__add_children(children)

    def __add_children(self, children):
        return self.notion.blocks.children.append(
            block_id=self.page_id, children=children
        )
