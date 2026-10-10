# Hilton Connected Room — Design Analysis
Reference: https://www.jbondy.com/work/hilton-connected-room/ (+ /work/room-controls for phone)
Assets: `~/workspace/bienvenue/reference/hilton/` (18 screenshots + 66s video) and `../hilton-phone/` (9 phone screenshots)
Date: October 10, 2026

## What they built
Designer Jean-Paul Bondy built the UX/UI from zero for Hilton's connected in-room experience:
check-in/out, customizable TV, hotel amenities, room controls (thermostat, lighting, sleep timer),
all rolling out to a planned 800,000 rooms (3,800 live, Garden Inn → Waldorf Astoria).
A companion phone experience (Hilton Honors app) adds mobile key, TV remote, and full room controls.

---

## 1. Welcome screen
**Pattern** (consistent across Tru, Tapestry, Waldorf Astoria):
- Full-bleed property photography, **no blur, no dim** — text legibility comes from photo
  choice (dark areas behind text) plus a subtle text shadow.
- Brand logo top-left. **Weather top-right, always**: temp + icon + weekday + time (e.g. "63° ☀ Wednesday 8:32P").
- Centered: "WELCOME" in small letterspaced caps, then the **guest name HUGE** (bold sans, ~10% of screen height).
- Bottom-center: a small circular **down-chevron** — press down to enter. No "press any key" text.

**Takeaways for Bienvenue**
- Our welcome concepts were directionally right (esp. #1 Maison Classic), but Hilton goes
  *bigger* on the name and keeps weather persistent in the corner — we should do both.
- The down-chevron is cleaner than a text hint; it teaches the exact key to press.
- Full-brightness photo (not dimmed) feels more premium than our instinct to scrim everything.

## 2. Home screen
**Pattern:**
- Top tabs (**Home / Entertainment**), not a sidebar or grid of sections. Weather top-right persists.
- **Hero carousel** with property content ("Canopy Bikes", "Evening Tastings"), title + subtitle +
  "Learn More" button + pager dots.
- **"Trending" row**: streaming apps as branded tiles (Netflix, Showtime, iHeart, YouTube) + live TV guide.
- **"Room Controls" row**: two-line tiles — **label on top, icon + live state on bottom**
  ("Climate control" / 🌡 73°; "Bedroom" / 💡 Off). State is glanceable without opening anything.
- Focused tile gets a blue highlight treatment.

**Takeaways for Bienvenue**
- Their home is **content-forward** (hero + labeled rows); ours is a tile grid. A hero would give
  our home more warmth and hierarchy.
- **Room-control tiles show live state inline** — our homepage tiles don't surface light/climate
  state at all; guests must open Your Room to see anything. Even a tiny "2 on" badge would help.
- Top tabs are simpler than our section-per-tile model, but our model fits a home (fewer
  sections) better than a hotel (many amenities). Not a change to chase.

## 3. Room controls (TV)
**Pattern** — the best part:
- The **focused card expands** to reveal actions, each labeled with its remote key:
  `Ok Turn off` / `↕ Adjust temperature` / `↩ Exit`. The key hints teach the remote inline —
  no manual needed.
- Climate card: big temperature with up/down chevrons, mode icon (blue thermometer),
  actions listed below.
- Unfocused cards collapse to label + state ("Sleep timer / Off").
- A separate illustration frame shows the same idea for lights: "Ok Turn off Bedroom light"
  appears above the Room Controls row when a light is focused.

**Takeaways for Bienvenue**
- **Steal the key-hint pattern.** Our room panel has no "Ok toggles / ↕ adjusts" teaching;
  guests discover by trial. Inline hints ("Ok Turn off", "↕ Adjust") would fix that in one line per tile.
- **Collapsible cards**: our climate panel is always fully expanded; Hilton's collapse/expand
  on focus keeps the row scannable and rewards focus with detail. Worth trying on our lamp tiles.
- State-first tile design (label + live state, no action needed to read it).

## 4. Phone handover (reference for later)
**Pattern** (`/work/room-controls`):
- Same dark theme and card language as the TV — one design system, two surfaces.
- **Room picker first**: "Welcome to Smart Room / Select the room you're in" (Rm 3049, Rm 3050…).
  Multi-room from one phone.
- Room controls as **horizontal cards** (icon + state top, label bottom) — same two-line tile
  as TV, rotated.
- **Floating remote button** (blue circle, bottom-right) — the TV remote lives one tap away.
- Streaming apps get hero cards; Live TV is a row.

**Takeaways for Bienvenue (future phone version)**
- Don't redesign for phone — **rotate the TV's card language**, keep the theme.
- Room picker matters the day we have more than one TV.
- The remote-as-FAB is the right call when we build phone control.

---

## Comparison: Hilton vs Bienvenue

| Area | Hilton | Bienvenue (today) | Adopt? |
|---|---|---|---|
| Welcome name size | Huge, centered, the whole moment | (concepts pending) | ✅ Go bigger |
| Welcome weather | Persistent top-right | Not on welcome concepts | ✅ Add it |
| Welcome enter affordance | Down-chevron icon | "Press any key" text | ✅ Chevron |
| Welcome photo treatment | Full brightness, no scrim | We tend to scrim .60 | ⚠️ Try brighter |
| Home structure | Hero + labeled rows + top tabs | Tile grid | 🤔 Hero yes, tabs no |
| Room tile state | Label + live state always visible | State hidden until panel opens | ✅ Surface state |
| Focused card | Expands with key-hinted actions | Static focus ring | ✅ Key hints + expand |
| Remote teaching | Inline ("Ok Turn off") | None | ✅ Inline hints |
| Phone | Same language, room picker, remote FAB | Future | 📌 Reference |

## Proposed next steps (for Alex to approve)
1. **Welcome screen**: revise concepts with huge name, persistent weather, down-chevron, brighter photo.
2. **Room panel**: add inline key hints ("Ok …", "↕ …") and try collapsible lamp tiles.
3. **Homepage tiles**: surface live light/climate state (badges) without opening panels.
4. Phone: file this analysis; revisit when we build it.
