class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if len(self.children) > 0:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)

            if self.text:
                internal = "%s" % self.text
            else:
                internal = ""

            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag

            return opening + internal + ending

        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)

            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text)

class HTML:

    def __init__(self, output = None):
        self.output = output
        self.childrens = []

    def __enter__(self):
        return self

    def __add__(self, other):
        self.childrens.append(other)
        return self

    def __exit__(self, *args):
        print("<html>")

        for child in self.childrens:
            print(str(child))
            
        print("</html>")

class TopLevelTag:

    def __init__(self, tag):
        self.tag = tag
        self.childrens = []

    def __enter__(self):
        return self    

    def __add__(self, other):
        self.childrens.append(other)
        return self

    def __str__(self):

        start = "<{tag}>".format(tag = self.tag)
        
        mid = ""
        for child in self.childrens:
            mid += str(child)

        end = "</{tag}>".format(tag = self.tag)

        return start + mid + end

        
    def __exit__(self, *args):
        return self


with HTML(output=None) as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png") as img:
                div += img

            body += div

        doc += body