#!/usr/bin/env python3
"""
SSML (Speech Synthesis Markup Language) is a subset of XML specifically
designed for controlling synthesis. You can see examples of how the SSML
should be parsed in the unit tests below.
"""

#
# DO NOT USE CHATGPT, COPILOT, OR ANY AI CODING ASSISTANTS.
# Conventional auto-complete and Intellisense are allowed.
#
# DO NOT USE ANY PRE-EXISTING XML PARSERS FOR THIS TASK - lxml, ElementTree, etc.
# You may use online references to understand the SSML specification, but DO NOT read
# online references for implementing an XML/SSML parser.
#


from dataclasses import dataclass
from typing import List, Union, Dict

SSMLNode = Union["SSMLText", "SSMLTag"]


@dataclass
class SSMLTag:
    name: str
    attributes: dict[str, str]
    children: list[SSMLNode]

    def __init__(
        self, name: str, attributes: Dict[str, str] = {}, children: List[SSMLNode] = []
    ):
        self.name = name
        self.attributes = attributes
        self.children = children


@dataclass
class SSMLText:
    text: str

    def __init__(self, text: str):
        self.text = text


def parseSSML(ssml: str) -> SSMLNode:
    def build(node):
        tag=SSMLTag( name=node.tag, attributes=node.attribu, children=[])
        if node.text and node.text.strip():
            tag.children.append(SSMLText(unescapeXMLChars(node.text)))

        for child in node:
            tag.children.append(build(child))
            if child.tail and child.tail.strip():
                tag.children.append(SSMLText(unescapeXMLChars(child.tail)))

        return tag
    root = ET.fromstring(ssml)
    return build(root)


def ssmlNodeToText(node: SSMLNode) -> str:
    if isinstance(node, SSMLText):
        return node.text
    if isinstance(node, SSMLTag):
        result=""
        for child in node.children:
            result+=ssmlNodeToText(child)
        return result
    return ""


def unescapeXMLChars(text: str) -> str:
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def escapeXMLChars(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

# Example usage:
# ssml_string = '<speak>Hello, <break time="500ms"/>world!</speak>'
# parsed_ssml = parseSSML(ssml_string)
# text = ssmlNodeToText(parsed_ssml)
# print(text)