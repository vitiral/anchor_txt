This is an ultra-simple library for splitting up markdown into component pieces
that are "interesting" for a machine to parse.

This library is intended to enable using markdown for storing data more
generally, i.e. putting attributes of the markdown in code blocks and using
tags intelligently.

# API

Calling `mdsplit.split(md_text)` returns a list of tokens of the following
types:
- HEADER: A `#+\w+` section. Contains `raw` (the entire header), `anchor` which is any defined
  link-anchors (i.e. `{#my-anchor}) and `text` which is `raw` stripped of
  the anchor text. Headers directly next to eachother will be joined (as they are in markdown).
- CODE: contains `raw` (the entire code block), `idenitifer` which is any text
  after the initial " \`\`\`" fence, and `text` which is `raw` stripped of any
  fences or identifiers. Indented code blocks are also parsed. They will have
  empty identifier and `text` is de-indented.
- TEXT: contains only `raw`, which is the raw text between identifiers.

The basic premise is that if you join the `raw` from all the tokens you will
have the original markdown.

To this end, `mdsplit.join(md_tokens)` will do exactly that.
