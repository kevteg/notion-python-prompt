from notion_client import Client


class NotionPython:

    prompt = ">>>"

    def __init__(self, token, page_id):
        """
        page_id: page to be used as the python 'interpreter'
        """
        self.notion = Client(auth=token)
        self.page_id = page_id

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
                    code = code.replace("Ó", "'")
                    break
        return code

    def eval_code(self):
        children = self.page_children()
        code = self.get_code(children)
        result = str(eval(code))
        result = result.replace("\n", "")
        print(result)
        self.add_result(result)

    def add_result(self, result):
        """adds the result and the prompt"""
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
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": self.prompt,
                            },
                        },
                    ],
                },
            },
        ]

        return self.notion.blocks.children.append(
            block_id=self.page_id, children=children
        )
