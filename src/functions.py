from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception("Invalid markdown: unmatched delimeter")

        for index in range(len(split_node)):
            part = split_node[index]
            if part == "":
                 continue
            if index % 2 == 0:
                new_text_node = TextNode(part, TextType.TEXT)
                new_list.append(new_text_node)
            else:
                new_delimeter_node = TextNode(part, text_type)
                new_list.append(new_delimeter_node)
    return new_list

