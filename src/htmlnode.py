class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise exception(NotImplementedError)

    def props_to_html(self):
        full_string = ""
        if self.props is None or self.props == {}:
            return ""
        for i in self.props:
            full_string += f' {i}="{self.props[i]}"'
        print(full_string)
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"