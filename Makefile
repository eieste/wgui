set-version:
	sed -i 's/__version__ = ".*"/__version__ = "$(NEW_VERSION)"/g' wgui/__init__.py
	sed -i 's/version=".*"/version="$(NEW_VERSION)"/g' setup.py
	sed -i 's/'release = \'*.\'/release = \'$(NEW_VERSION)\'/g docs/source/setup.py


build:
	tailwindcss -i src/css/tailwind.css -o wgui/static/css/tailwind.css
