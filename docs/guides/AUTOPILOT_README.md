# UwU-CLI Autopilot System 🚀

The autopilot system provides real-time notifications for your UwU-CLI activities via Telegram, Email, and Feishu.

## 🎯 What It Does

- **CLI Start/Stop Notifications**: Get notified when UwU-CLI starts or exits
- **Command Execution Tracking**: Monitor which commands are run and their success/failure
- **Error Notifications**: Receive alerts when errors occur
- **Custom Messages**: Send your own notifications through the system
- **Remote Control via Telegram**: Control UwU-CLI from your phone
- **Cursor Editor Integration**: Open files and folders in Cursor directly

## 🚀 How to Use

### 1. Basic Usage

The autopilot is automatically integrated into UwU-CLI and will:

- Send a notification when you start the CLI
- Send a notification when you exit the CLI
- Track command execution (if configured)

### 2. Manual Commands

In UwU-CLI, you can use these commands:

```bash
# Test the autopilot system
autopilot:test

# Check autopilot status
autopilot:status

# Telegram control commands
telegram:start    # Start remote command control
telegram:stop     # Stop remote command control
telegram:status   # Check Telegram control status
```

### 3. Remote Control via Telegram 🎮

**NEW FEATURE!** You can now control UwU-CLI remotely from your phone!

#### How it works:

1. **Start UwU-CLI** - Telegram control activates automatically
2. **Send commands to your bot** - Any text you send becomes a CLI command
3. **Get results instantly** - Bot sends back command output

#### Bot Commands:

- `/start` - Show help and welcome message
- `/status` - Check if controller is running
- `/help` - Show help information

#### Example Usage:

```
You send: ls -la
Bot replies: 🔄 Executing: ls -la
Bot replies: ✅ Result: [command output]

You send: pwd
Bot replies: 🔄 Executing: pwd
Bot replies: ✅ Result: /current/directory
```

### 3. Programmatic Usage

You can also use the autopilot in your own scripts:

```python
from utils.autopilot import send_notification, get_autopilot

# Send a simple notification
send_notification("Hello from my script!", "Custom Title")

# Get autopilot instance for more control
autopilot = get_autopilot()
autopilot.notify_command_executed("my_command", True)
autopilot.notify_error("Something went wrong", "My Script")
```

## 📱 Available Adapters

### Telegram ✅ (Currently Active)

- Sends messages to your Telegram chat
- Real-time notifications
- Emoji support
- HTML formatting

### Email 📧 (Configured)

- Sends emails via Gmail SMTP
- Subject line support
- Plain text formatting
- Reliable delivery

### Feishu 🐦 (Configured)

- Sends messages via Feishu API
- Enterprise-grade notifications
- Webhook support available

## ⚙️ Configuration

Your `.autopilot.json` file controls:

- Which services are enabled
- API keys and credentials
- Notification preferences

### Enable/Disable Services

```json
{
  "enabled": true,
  "adapters": ["telegram", "email", "feishu"]
}
```

### Add New Services

To add a new notification service:

1. Add it to the `adapters` array
2. Add configuration section
3. Implement the service in `utils/autopilot.py`

## 🧪 Testing

### Test Autopilot Notifications

Run the test script to verify everything works:

```bash
python test_autopilot.py
```

This will:

- Test all configured services
- Send sample notifications
- Verify connectivity
- Show status information

### Test Telegram Command Control

Test the remote control feature:

```bash
python test_telegram_control.py
```

This will:

- Start the Telegram controller
- Allow you to send commands via Telegram
- Test command execution and responses
- Verify remote control functionality

**💡 Tip**: Keep this running and send messages to your bot to test remote control!

### Test Cursor Editor Control

Test the Cursor integration:

```bash
python test_cursor_control.py
```

This will:

- Check Cursor availability
- Test opening files and folders
- Test Cursor window management
- Verify integration functionality

**💡 Tip**: Make sure Cursor editor is installed to test all features!

### Test Cursor Command Sending

Test the new Cursor command features:

```bash
python test_cursor_commands.py
```

This will:

- Test sending commands to Cursor
- Test sending keyboard shortcuts to Cursor
- Test custom command handling
- Verify command integration functionality

**💡 Tip**: This tests the ability to control Cursor from UwU-CLI!

## 🔧 Troubleshooting

### Common Issues

1. **Telegram not working**

   - Check bot token and chat ID
   - Ensure bot is started in Telegram
   - Verify bot has permission to send messages

2. **Email not working**

   - Verify Gmail app password
   - Check SMTP settings
   - Ensure 2FA is enabled

3. **Feishu not working**
   - Verify app ID and secret
   - Check app permissions
   - Ensure app is approved

### Debug Mode

Enable debug logging by modifying the autopilot module:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 📋 Notification Types

### Built-in Notifications

- **CLI Start**: 🚀 UwU-CLI started at [timestamp]
- **CLI Exit**: 👋 UwU-CLI exited at [timestamp]
- **Command Success**: ✅ Command executed: [command]
- **Command Failure**: ❌ Command executed: [command]
- **Error**: 🚨 Error in [context]: [error]

### Custom Notifications

Send any message with custom title:

```python
send_notification("Your custom message here!", "Custom Title")
```

## 🎨 Customization

### Message Formatting

- Use emojis for visual appeal
- Include timestamps for tracking
- Add context information
- Use line breaks for readability

### Notification Frequency

Control when notifications are sent:

- Only on errors
- On every command
- On specific events
- Custom triggers

## 🔒 Security Notes

- Keep your `.autopilot.json` file secure
- Don't commit credentials to version control
- Use app passwords for email services
- Regularly rotate API keys

## 🚀 Future Features

Planned enhancements:

- Notification scheduling
- Message templates
- Rate limiting
- Notification history
- Web dashboard
- Mobile app integration

---

**Happy notifying! 🎉**
