class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        props_string = ""
        if self.props is None or self.props == {}:
            return ""
        for i in self.props:
            props_string += f' {i}="{self.props[i]}"'
        return props_string
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag = tag, value = value, children = None, props = props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag = tag, children = children, props = props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        elif self.children == []:
            raise ValueError("ParentNode must have a child")
        else:
            children_html = "".join(child.to_html() for child in self.children)
            if self.props is not None:
                prop_string = self.props_to_html()
                return f'<{self.tag}{prop_string}>{children_html}</{self.tag}>'
            return f'<{self.tag}>{children_html}</{self.tag}>'