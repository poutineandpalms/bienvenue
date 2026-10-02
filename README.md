# Bienvenue

A hotel-style welcome screen for a Samsung Tizen TV (guest room). Guests get a
personalized greeting, local time and weather, streaming app shortcuts, and —
when the TV is on the home network — live control of the guest room lights via
Home Assistant.

## Preview
Open `index.html` in any browser (or GitHub Pages) to iterate on the layout.
TV-only features (app launching) and Home Assistant controls stay dormant
outside the TV — everything else renders as guests will see it.

## Configuration
All guest-visible content lives in `config.js` (greeting, cast device name,
light entities, weather location). The Home Assistant token is never committed:
it is injected by `local-config.js` (gitignored) only in the TV build.

## TV build
Package `index.html`, `config.js`, `config.xml`, `icon.png` (plus the generated
`local-config.js`) as a Tizen web widget. App ID: `Bienvenue1.Bienvenue`.
