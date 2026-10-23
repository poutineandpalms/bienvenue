/* Bienvenue — app configuration (structure only).
   Guest CONTENT (names, heroes, plan, guide) is NOT baked into the build:
   it loads from the stay-app content endpoints at runtime (see the content
   engine in index.html), with the last-good payload cached on the device.
   The HA token is NEVER in this file — it is injected by local-config.js
   (gitignored, generated only for the TV build). */
window.BIENVENUE_CONFIG = {
  guestName: "",
  /* Welcome screen names — shown big on launch. Override in local-config.js. */
  welcomeNames: "",
  tagline: "",
  castName: "Guest Bedroom TV",
  contentOrigin: "https://stay.withalex.link",
  homeAssistantUrl: "http://192.168.0.98",
  homeAssistantToken: null,
  /* Wi-Fi join details are NEVER committed — they ride in local-config.js
     (gitignored, TV build only) as: wifi: { ssid: "...", password: "...", auth: "WPA" } */
  wifi: null,
  /* Tricount live folio — also local-config.js only (the share key is a
     capability link): tricount: { key: "...", member: "Alexandr", publicKey: "-----BEGIN RSA PUBLIC KEY-----\n..." } */
  tricount: null,
  lights: [
    { entity: "light.bedside_left", label: "Bedside Left", icon: "🛏️" },
    { entity: "light.corner_lamp_bedroom", label: "Corner Lamp", icon: "💡" },
    { entity: "light.floor_lamp", label: "Floor Lamp", icon: "🔆" }
  ],
  switches: [
    { entity: "switch.bedroom_scent_diffuser_socket_1", label: "Scent Diffuser", icon: "💨" }
  ],
  weather: { lat: 28.29704, lon: -81.59847, label: "Kissimmee" },
  /* Guest thermostat limits (Celsius) — enforced in 0.5° steps. Cooling season
     guests stay within [coolMin, coolMax]; heating season within [heatMin, heatMax]. */
  climate: { entity: "climate.my_ecobee", coolMin: 21, coolMax: 25, heatMin: 17, heatMax: 21 },
  /* Welcome (splash) reset behaviour. The app process survives TV standby,
     so without this it would resume on a stale screen for days. "smart":
     re-show the welcome screen when the app returns after >= afterHours
     away, or on its first appearance of a new day; short absences resume
     where the guest left off. "always": welcome on every launch/foreground.
     "never": only the very first launch. */
  splashReset: { mode: "smart", afterHours: 2 },
  /* Welcome splash video (muted, looping): replaces the photo rotation on
     the listed local dates. "force" shows it regardless of date (preview
     only — set back to false after the preview is approved). */
  welcomeVideo: { src: "https://build.withalex.link/bienvenue/app/assets/heroes/mnsshp-sunday-v2.mp4", dates: ["2026-10-25"], force: true }
};
