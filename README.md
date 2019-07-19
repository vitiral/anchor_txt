anchor_txt: attributes in markdown

anchor_txt adds the ability to embed attributes in markdown files so that external
tools can more easily link them to eachother and code, as well as perform
other operations.

Use ``anchor_txt.Section.from_md_path`` to load a markdown file.

# Markdown Syntax
The syntax for anchor_txt attributes is simple.

- Headers of the form `# header {#anchor}` will have the `anchor` tag extracted and available
  in `Header.anchor`
- A header creates a Section, which can have sub `sections`.
- Sections have attributes, which are embedded yaml either inline or in fenced
  code blocks, shown below.

An inline attribute looks like one of these:
```
`@{foo}`
`@{bar: 2}`
```

Fenced code block attributes look like below. They must include the identifier
`yaml` (or `json`) and end with a `@`

    ```yaml @
    foo: null
    bar: 2
    ```

Attributes blocks within a Section are combined through the same process as
`dict.update`, except overlapping keys throw an error.

# Developer
Run `make init` to create the necessary virtualenv

Run `make test` for basic tests or `make check` for lints and formatting.


# License

The source code is Licensed under either of

* Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
  http://www.apache.org/licenses/LICENSE-2.0)
* MIT license ([LICENSE-MIT](LICENSE-MIT) or
  http://opensource.org/licenses/MIT)

at your option.

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.
