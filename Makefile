# Python Code Style
reformat:
	black -l 99 `git ls-files "*.py"`
stylecheck:
	black --check -l 99 `git ls-files "*.py"`

# Translations
gettext:
	redgettext --command-docstrings --verbose --recursive Thinslaves --exclude-files "Thinslaves/pytest/**/*"
upload_translations:
	$(MAKE) gettext
	crowdin upload sources
download_translations:
	crowdin download
