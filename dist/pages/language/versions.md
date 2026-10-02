# [Language Versions and Migration](#language-versions-and-migration)

An MDL script is written in one **language version**, declared by its first
statement:

```
mdl 1;

create persistent entity Shop.Customer (
  Name: String(200)
);

```

A script file with no header is **mdl 0**, the alpha language. The rest of
this manual documents `mdl 1`; this page is the one place that documents what
`mdl 0` means differently, and how to move a script from one to the other.

Two rules make the move safe ([ADR-0011](https://github.com/mendixlabs/mxcli/blob/main/docs/13-decisions/0011-mdl-language-versioning.md)):

- **A script never changes meaning because a newer mxcli runs it.** A change of
  meaning, or a new rejection, applies only under the header that introduces
  it. Without the header the old meaning is kept, and the construct warns with
  an `MDL-V1-*` code.
- **A deprecated spelling is a respelling.** It means exactly what its new form
  means, warns with an `MDL-DEPR*` code, and `mxcli fmt --upgrade` rewrites it.
  It is refused only from the version named in its entry.

Every warning that carries one of these codes ends with a pointer such as
`(mxcli help MDL-V1-LIMIT1)`. That command prints the code’s entry: the old
form, the new form, whether `fmt --upgrade` rewrites it, and the version that
refuses it. `mxcli syntax <topic> --deprecated` lists the old spellings of one
topic.