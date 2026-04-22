# UI Patch Instructions

## 1. Copy files into Boundary app folder
Copy into your existing `app/` folder:
- `ui_enforcement_upgrade.js`
- `ui_enforcement_upgrade.css`

## 2. Load CSS and JS in `app/index.html`
Add in the `<head>`:
```html
<link rel="stylesheet" href="./ui_enforcement_upgrade.css">
```

Add near the end of `<body>`, after `enforcement_connector.js`:
```html
<script src="./ui_enforcement_upgrade.js"></script>
```

## 3. Replace raw forwarding call
If you currently use:
```javascript
forwardBoundaryResult(result, selectedDomain);
```

replace it with:
```javascript
forwardBoundaryResultWithUI(result, selectedDomain);
```

## 4. Result
The UI will now show:
- whether forwarding is enabled
- endpoint in use
- last state forwarded
- forwarding response
- buttons for enable, disable, and test payload

## 5. Safe default
Forwarding is still disabled unless you enable it.
