/* Bienvenue — content configuration.
   Everything guests see comes from here (design lives in index.html).
   The HA token is NEVER in this file — it is injected by local-config.js
   (gitignored, generated only for the TV build). */
window.BIENVENUE_CONFIG = {
  guestName: "Monique",
  tagline: "Make yourself at home — everything you need is right here.",
  castName: "Guest Bedroom TV",
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
  weather: { lat: 28.29704, lon: -81.59847, label: "Kissimmee" },
  /* Guest thermostat limits (Celsius) — enforced in 0.5° steps. Cooling season
     guests stay within [coolMin, coolMax]; heating season within [heatMin, heatMax]. */
  climate: { entity: "climate.my_ecobee", coolMin: 21, coolMax: 25, heatMin: 17, heatMax: 21 }
};
