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
  lights: [
    { entity: "light.bedside_left", label: "Bedside Left", icon: "🛏️" },
    { entity: "light.corner_lamp_bedroom", label: "Corner Lamp", icon: "💡" },
    { entity: "light.floor_lamp", label: "Floor Lamp", icon: "🔆" }
  ],
  weather: { lat: 28.29704, lon: -81.59847, label: "Kissimmee" }
};
