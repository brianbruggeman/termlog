========
Changes
========


1.3.4
-----
* Updates CI/CD process
* Adds Github Actions
* Removes Travis CI/CD


1.3.3
-----
* Fixes multi-line and f-string embeds


1.3.0
-----
* Now uses Poetry as a build dependency
* Upgrades to pyproject.toml
* Uses Black for style control


1.2.1
-----
* Drops build field from __metadata__.py


1.2.0
-----
* Migrates config to its own file
* Format now produces json based on config
* Small tweaks to documentation
* Hopefully benign update to the inspection/frame crawling logic to capture more data for json output


1.1.1
-----
* Bug fix for indentation squashing
* Adds strip to palette to remove escape characters
* Bug fix for style


1.1.0
-----
* Drops extraneous color functions and now uses colors directly
* Adds support for dim
* Normalizes colors to use standard ansi color codes unless explicitly calling truecolor
* Adds demo script
* Adds palettes


1.0.2
-----
* Fixes travis bugs


1.0.1
-----
* Fixes test bugs

1.0
---

* Initial beta release
