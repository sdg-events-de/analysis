# Helper class for parsing a HTML/CSS object
class Parser:
    def __init__(self, css_object, response):
        self.css_object = css_object
        self.response = response

    # Appends default_selector (such as ' *::text') to the query, unless
    # the query already has a selector set
    def format_selector(self, query, default_selector):
        is_exact_query = "::" in query

        if is_exact_query:
            return query
        else:
            return query + default_selector

    def join_texts(self, texts):
        return u"\n".join(texts).strip()

    def extract_href(self, tag):
        full_selector = self.format_selector(tag, " *::attr(href)")
        url = self.css(full_selector).get(default="").strip()
        return self.full_url(url)

    def extract_text(self, tag):
        return self.join_texts((self.extract_text_list(tag)))

    def extract_text_list(self, tag):
        full_selector = self.format_selector(tag, " *::text")
        return map(lambda x: x.strip(), self.css(full_selector).getall())

    def full_url(self, url):
        if url is None:
            return None

        return self.response.urljoin(url)

    def css(self, *args, **kwargs):
        return self.css_object.css(*args, **kwargs)