# SecondLine visual references

Observed directly in a browser on 2026-09-30 KST at an approximately 985 × 720 desktop viewport. These are commercial products in the adjacent call and scam protection category. SecondLine is a fictional spoken rehearsal, not an incoming-call detector.

## Truecaller Scam Checker

- Product screen: [Truecaller Scam Checker](https://www.truecaller.com/scam-checker). The visible top navigation led here from [Truecaller Scam Alert](https://www.truecaller.com/scam-alert).
- **Visible composition:** once the page finished loading, the desktop hero was a full-width saturated royal-blue photographic panel: brand at upper left, a large white left-aligned headline, a woman looking at a phone on the right, and a wide white search pill with a blue “Check now” button. A small trust claim sits above the headline. Below the hero begins the community feed under a bold centered heading. Feed cards show author, post, reactions, and comments, with “Popular” sort and “Load more posts” for browsing.
- **Typography and density:** bold modern sans for a high-contrast headline; compact metadata and small legal text under the search field. The first viewport spends most space on one promise and the search action, then the community index appears below.
- **Interaction rule observed:** search is the first action; sort and post links follow. The product describes checking numbers/URLs and reading community posts, not rehearsing a spoken boundary. The search control also exposes a Terms of Service and Privacy Policy notice; SecondLine has no equivalent external lookup action.
- **Use for SecondLine:** a visible service status and clear primary action. **Avoid:** community counts, a scam score, or wording that implies a fictional drill has verified a real caller.

## Hiya Spam Blocker

- Product screen: [Hiya Spam Blocker](https://www.hiya.com/products/apps/hiya-spam-blocker). Opened from Hiya’s visible Products navigation after an old `/products/hiya-protect` link returned a 404.
- **Visible composition:** quiet off-white/lavender hero with a roomy split layout. Left side uses a small app mark and product name, a large two-line black headline with a purple-to-blue accent on the second line, a brief support sentence, two strong black app-store buttons, then review/download proof. An animated phone mockup fills the right side; while observed it cycled from call screening with “Take Over”/“Hang Up” actions to a red “Fraud Call Detected” warning and dismissal button. Navigation has broad horizontal spacing and few top-level categories.
- **Typography and density:** heavy modern sans headline, smaller gray support copy, clear hierarchy from promise to download to proof. The first viewport has one claim and one phone state. Lower on the page, three feature blocks pair “Identifying Unknown Callers,” “Detecting Fake Voices,” and “Stopping Fraud Attempts” with short copy and “Play now” demonstrations.
- **Interaction rule observed:** the hero communicates active-call control immediately; feature demos disclose behavior one step at a time. The call-screen image is the main visual proof, not an analytics dashboard.
- **Use for SecondLine:** unmistakable state changes during a single exercise, a large readable action, and an on-screen transcript as proof of what happened. **Avoid:** copying Hiya’s phone mockup, logo, purple gradient, live-call detection promise, or any unsupported adoption numbers.

## SecondLine direction and boundaries

SecondLine uses a warm paper background (`#f5f2e9`), deep evergreen active session (`#102926`), coral action (`#ea7259`), and restrained lime guidance (`#d5e58d`). Fraunces is used for the human, editorial headline; DM Sans carries controls and transcript text. A visible hero link jumps directly to the 60-second exercise, showing all three scenarios and the primary voice action in a 1280 × 720 browser view. The exercise reads as a field card with a listening/speaking area and adjacent three-step guide. The reflection beneath it uses the learner’s captured words and literal pressure phrases. The offline typed walkthrough is visibly separate. No third-party logo, proprietary image, font file, source code, or paid asset was copied.

Responsive rule: at desktop widths, scenario/exercise and field guide sit side by side; below 850 px the guide follows the exercise; below 640 px scenario cards become stacked, session actions fill the width, and transcript/coach panels flow vertically. Focus rings, keyboard buttons, semantic labels, ARIA pressed state, reduced-motion behavior, and status announcements support accessibility.

Browser note: the live microphone path requests echo cancellation and leaves browser noise suppression off because the voice service performs its own processing. The client resamples the browser's actual audio context rate to 24 kHz PCM16. `ScriptProcessorNode` is supported in current Chromium but deprecated; a real device and provider session are still needed to prove microphone, interruption, and playback behavior on each target browser.
