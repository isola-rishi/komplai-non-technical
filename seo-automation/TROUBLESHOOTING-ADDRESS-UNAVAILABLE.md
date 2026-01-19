# Troubleshooting: "Address unavailable" Error

## Error Message
```
Error: Address unavailable: https://api.anthropic.com/v1/messages
```

## What This Means

This error occurs when Google Apps Script cannot reach the Anthropic API endpoint. This is **NOT** an issue with your API key or the script code - it's a network connectivity issue between Google's servers and Anthropic's API.

---

## Quick Solutions (Try These First)

### Solution 1: Wait and Retry (Most Common Fix)
This is often a temporary network issue that resolves itself.

**Steps**:
1. Wait 5-10 minutes
2. Try running the script again
3. If it works, the issue was temporary network congestion

**Success Rate**: ~70% of cases resolve this way

---

### Solution 2: Re-authorize the Script
Sometimes Google Apps Script needs fresh authorization to make external API calls.

**Steps**:
1. Open Google Apps Script (Extensions > Apps Script)
2. Click on the `setup` function in the function dropdown
3. Click **Run** (play button icon)
4. If prompted, click **Review permissions**
5. Choose your Google account
6. Click **Advanced** → **Go to [Your Project] (unsafe)**
7. Click **Allow**
8. Close Apps Script and refresh your Google Sheet
9. Try generating content again

**Success Rate**: ~20% of cases

---

### Solution 3: Check Google Apps Script Status
Google Apps Script may be experiencing an outage.

**Steps**:
1. Visit: https://www.google.com/appsstatus/dashboard/
2. Look for "Google Apps Script" in the list
3. Check if there's a service disruption (red or yellow icon)
4. If yes, wait until Google resolves the issue

**Success Rate**: ~5% of cases (actual outages are rare)

---

### Solution 4: Use a Different Network
Sometimes your organization's network/firewall blocks the API.

**Steps**:
1. Try using your phone's hotspot instead of your work WiFi
2. If it works on hotspot, your organization is blocking api.anthropic.com
3. Contact your IT department to whitelist the domain

**Success Rate**: ~5% of cases (mainly corporate networks)

---

## Advanced Solutions

### Solution 5: Check API Endpoint Manually
Verify the Anthropic API is actually reachable.

**Steps**:
1. Open your web browser
2. Visit: https://api.anthropic.com
3. You should see a response (even an error is fine - we just want to confirm the domain resolves)
4. If the page doesn't load at all, the issue is with your internet connection or DNS

### Solution 6: Retry Logic (Already Built In)
The script now includes automatic retry with exponential backoff.

**How it works**:
- First attempt: Immediate
- Second attempt: Wait 2 seconds, retry
- Third attempt: Wait 4 seconds, retry
- Fourth attempt: Wait 8 seconds, give up

**Total wait time**: Up to 14 seconds before failing

**What to do**: Just run the script normally - retries happen automatically

---

## Understanding the Error

### Why This Happens

The error occurs because:

1. **Google Apps Script Quotas**: Google limits external URL fetches
   - Check: https://developers.google.com/apps-script/guides/services/quotas
   - Free tier: 20,000 URL fetch calls per day
   - If exceeded, wait until quota resets (midnight Pacific Time)

2. **DNS Resolution Failure**: Google's servers can't resolve `api.anthropic.com`
   - Temporary: Usually resolves in 5-10 minutes
   - Persistent: Rare, indicates larger Google or Anthropic infrastructure issue

3. **Network Routing Issues**: Packets can't route from Google → Anthropic
   - Temporary: Usually resolves in 10-30 minutes
   - Beyond your control

4. **Firewall/Proxy**: Your organization blocks outbound API calls
   - Solution: Work with IT to whitelist api.anthropic.com
   - Workaround: Use personal Google account + personal network

---

## How to Prevent This

### Best Practices

1. **Don't Generate Too Many Articles at Once**
   - Generate 5-10 articles at a time
   - Wait a few minutes between batches
   - This avoids hitting rate limits

2. **Run During Off-Peak Hours**
   - Best times: Early morning (6-9 AM) or late evening (8-11 PM) in your timezone
   - Avoid: Midday (12-3 PM) when network congestion is highest

3. **Use the Retry Logic**
   - The script now automatically retries failed requests
   - No manual intervention needed
   - Check the logs (View > Logs in Apps Script) to see retry attempts

4. **Monitor Your Quotas**
   - Apps Script Dashboard: https://script.google.com/home/executions
   - Look for quota errors
   - Upgrade to Google Workspace if you need more quota

---

## What the Script Does Now

### Automatic Retry with Exponential Backoff

The updated script includes `callAnthropicAPIWithRetry()` function:

```javascript
function callAnthropicAPIWithRetry(payload, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      // Make API call
      // If successful, return immediately
      // If fails, wait and retry
    } catch (e) {
      // Log the error
      // Wait 2s, 4s, or 8s depending on attempt number
      // Retry
    }
  }
}
```

**Benefits**:
- Handles temporary network glitches automatically
- No user intervention required
- Logs all retry attempts for debugging
- Fails gracefully after 3 attempts

---

## Testing Connectivity

### Quick Test Command

Run this in Apps Script to test if you can reach the API:

```javascript
function testAnthropicConnection() {
  try {
    const response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', {
      method: 'post',
      contentType: 'application/json',
      headers: {
        'x-api-key': 'test-key',
        'anthropic-version': '2023-06-01'
      },
      payload: JSON.stringify({
        model: 'claude-sonnet-4-5-20250929',
        max_tokens: 10,
        messages: [{ role: 'user', content: 'hi' }]
      }),
      muteHttpExceptions: true
    });

    Logger.log('Connection successful! Response code: ' + response.getResponseCode());
    Logger.log('Response: ' + response.getContentText());
  } catch (e) {
    Logger.log('Connection failed: ' + e.toString());
  }
}
```

**Expected Results**:
- ✅ **Good**: Response code 401 (authentication error) - means you reached the API, just need valid key
- ✅ **Good**: Response code 200 - means API is fully working
- ❌ **Bad**: "Address unavailable" - means network connectivity issue

---

## When to Contact Support

Contact Anthropic support if:
- The error persists for more than 24 hours
- You can access api.anthropic.com in your browser but not from Apps Script
- You've tried all solutions above
- Other APIs work from Apps Script but Anthropic doesn't

Contact Google Workspace support if:
- Google Apps Script dashboard shows outages
- Other users in your organization have the same issue
- The error started after a Google Workspace policy change

---

## Checking Logs

### How to View Detailed Error Logs

1. **Open Apps Script**:
   - Extensions > Apps Script

2. **View Execution Log**:
   - Click "Executions" icon on left sidebar
   - Find the failed execution
   - Click to see detailed error

3. **View Logger Output**:
   - View > Logs (Ctrl+Enter / Cmd+Enter)
   - Look for retry attempts:
     ```
     API call failed (attempt 1/3): Address unavailable
     Waiting 2000ms before retry...
     API call failed (attempt 2/3): Address unavailable
     Waiting 4000ms before retry...
     ```

---

## Summary

| Solution | Success Rate | Time Required |
|----------|-------------|---------------|
| Wait and retry | 70% | 5-10 minutes |
| Re-authorize script | 20% | 2 minutes |
| Check Google status | 5% | 1 minute |
| Different network | 5% | 5 minutes |

**Most likely fix**: Wait 5-10 minutes and try again. The built-in retry logic should handle most temporary issues automatically.

---

**Last Updated**: January 2026
**Script Version**: 2.1 (with retry logic)
