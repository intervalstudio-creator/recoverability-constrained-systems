# Engine Integration Notes

## Files
- medication_engine.js
- app/medication_demo.html
- scenarios/medication_failure_case.json

## Basic integration
1. Upload `medication_engine.js` to repo root or app assets path.
2. Upload `app/medication_demo.html` into your app folder.
3. Link the engine in your existing UI with:

```html
<script src="../medication_engine.js"></script>
```

## Demo
Open:
- app/medication_demo.html

Then:
- click `Load benzo failure preset`
- review decision, action, and reason codes
