# JJANJ: report the concrete base-release version instead of the
# semantic-release placeholder. The upstream v1.3.4 tag carries ``9999dev0``
# (the release build stamps the real version), so a Git install of the tag
# reports the placeholder. Step 7a bases this fork on v1.3.4, so stamp the
# matching release identity. Packaging only; no behaviour change.
__version__ = "1.3.4"
