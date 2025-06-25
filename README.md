# GoOsint - Gmail OSINT Tool

![GoOsint Banner](https://img.shields.io/badge/GoOsint-Gmail%20OSINT-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-Educational-red?style=for-the-badge)

A comprehensive Gmail OSINT (Open Source Intelligence) tool powered by GHunt for email reconnaissance and investigation.

## ⚠️ Legal Disclaimer

**This tool is for educational and legal OSINT purposes only.** Always ensure you have proper authorization before investigating any email addresses. The developers are not responsible for misuse of this tool.

## 🚀 Features

- **Email Investigation**: Comprehensive Gmail account reconnaissance
- **Batch Processing**: Investigate multiple emails from a file with clear separators
- **Automated Setup**: Easy GHunt installation and configuration
- **Colorful Output**: Beautiful terminal interface with colored output and proper spacing
- **Clean Interface**: GHunt banner is hidden for cleaner output
- **Enhanced Readability**: Improved spacing between sections and results
- **JSON Output**: Structured data storage in single JSON file for easy analysis
- **Organized Storage**: Results automatically saved in dedicated folder structure
- **Result Logging**: Automatic saving of investigation results with timestamps
- **Cross-Platform**: Works on Linux, macOS, Android (Termux), and Windows

## 📋 Requirements

- Python 3.7 or higher
- Internet connection
- Valid Google credentials for GHunt setup

**Platform Support:**
- Linux (all major distributions)
- macOS (10.12 or later)
- Android (via Termux)
- Windows (with WSL recommended)

## 🔧 Installation

### Method 1: Automated Installation (Recommended)

Run the installation script that automatically detects your environment:

```bash
# Make the script executable
chmod +x install.sh

# Run the installation
./install.sh
```

**Supported Platforms:**
- 🐧 **Linux** (Ubuntu, Debian, CentOS, Arch Linux)
- 🍎 **macOS** (with Homebrew)
- 🤖 **Termux** (Android)

### Method 2: Manual Installation

1. **Clone or download the repository:**
   ```bash
   git clone <repository-url>
   cd GoOsint
   ```

2. **Install dependencies:**
   ```bash
   # For Linux/macOS
   pip3 install -r requirements.txt
   
   # For Termux
   pip install -r requirements.txt
   ```

3. **Make the script executable:**
   ```bash
   chmod +x GoOsint.py
   ```

### Termux (Android) Specific Setup

For Android users using Termux:

1. **Install Termux** from F-Droid or Google Play Store

2. **Grant storage permissions:**
   ```bash
   termux-setup-storage
   ```

3. **Install required packages:**
   ```bash
   pkg update
   pkg install python git curl wget
   ```

4. **Run the automated installer:**
   ```bash
   ./install.sh
   ```

## ⚙️ Setup

Before using GoOsint, you need to set up GHunt authentication:

```bash
python3 GoOsint.py --setup
```

This will guide you through the GHunt authentication process, which requires:
- A Google account
- Browser authentication
- Cookie extraction

## 📖 Usage

### Display Help
```bash
python3 GoOsint.py --help
```

### Investigate Single Email
```bash
python3 GoOsint.py -e target@gmail.com
```

### Batch Investigation
Create a text file with one email per line:
```
target1@gmail.com
target2@gmail.com
target3@gmail.com
```

Then run:
```bash
python3 GoOsint.py -f email_list.txt
```

### Install/Reinstall GHunt
```bash
python3 GoOsint.py --install
```

### Run Without Banner
```bash
python3 GoOsint.py --no-banner -e target@gmail.com
```

## 📊 Output

GoOsint provides detailed information about Gmail accounts including:
- Account existence verification
- Profile information (if available)
- Associated Google services
- Public information exposure
- And more...

**Clean Interface**: The GHunt banner is automatically hidden to provide a cleaner, more professional output while maintaining all the colorful status indicators and results formatting.

**JSON Output**: All investigation results are automatically saved to a single JSON file with structured data including:
- Session information (start/end times, total investigations)
- Individual investigation results with parsed data
- Profile information (email, Gaia ID, profile pictures, last edit dates)
- Google services data (Maps, Chat, YouTube, etc.)
- Raw output for complete reference
- Error handling for failed investigations

Results are saved as `goosint_results/investigation_YYYYMMDD_HHMMSS.json` in a dedicated folder for better organization.

## 🛠️ Command Line Options

| Option | Description |
|--------|-------------|
| `-e, --email` | Investigate a single email address |
| `-f, --file` | Batch investigate emails from file |
| `-s, --setup` | Setup GHunt authentication |
| `-i, --install` | Install/reinstall GHunt |
| `--no-banner` | Skip banner display |
| `-h, --help` | Show help message |

## 📁 File Structure

```
goosint/
├── GoOsint.py               # Main application
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── email_list.txt          # Sample email list for batch processing
└── results/        # Investigation results folder (auto-created)
    ├── investigation_*.json # Individual investigation sessions
    └── ...
```

## 📄 JSON Output Structure

GoOsint saves all results in a structured JSON format:

```json
{
  "session_info": {
    "start_time": "2025-06-25T07:08:38.186686",
    "tool_version": "1.0",
    "total_investigations": 3,
    "end_time": "2025-06-25T07:08:46.108719"
  },
  "investigations": [
    {
      "email": "target@gmail.com",
      "timestamp": "2025-06-25T07:08:41.296830",
      "status": "success",
      "profile": {
        "email": "target@gmail.com",
        "gaia_id": "118416446611115164332",
        "profile_picture": "https://...",
        "last_edit": "2025/06/21 20:24:02 (UTC)"
      },
      "services": {
        "chat_entity_type": "PERSON",
        "enterprise_user": "False",
        "activated_services": ["Youtube", "Photos", "Maps", "Meet"],
        "maps_profile": "https://...",
        "maps_reviews": "7"
      },
      "raw_output": ["...", "..."]
    }
  ]
}
```

## 🔍 What Information Can Be Gathered?

GoOsint (via GHunt) can potentially reveal:
- **Account Status**: Whether the Gmail account exists
- **Profile Information**: Name, profile picture, account creation date
- **Google Services**: Associated YouTube, Google+, Google Photos accounts
- **Public Information**: Publicly available data linked to the account
- **Account Activity**: Last seen information (if available)

## 🚫 Limitations

- Only works with Gmail addresses
- Requires Google authentication setup
- Limited by Google's privacy settings
- Some information may not be available for all accounts
- Rate limiting may apply for bulk investigations

## 🛡️ Privacy & Ethics

- **Always obtain proper authorization** before investigating
- Respect privacy and applicable laws
- Use only for legitimate OSINT purposes
- Do not use for harassment or malicious activities
- Be aware of local and international privacy laws

## 🐛 Troubleshooting

### GHunt Not Working
1. Ensure GHunt is properly installed: `python3 GoOsint.py --install`
2. Reconfigure authentication: `python3 GoOsint.py --setup`
3. Check internet connection
4. Verify Google account permissions

### Permission Errors
- Ensure Python has necessary permissions
- Run with appropriate user privileges
- Check file/directory permissions

### Dependencies Issues
```bash
pip install --upgrade -r requirements.txt
```

### Termux (Android) Specific Issues

#### Storage Access Problems
```bash
termux-setup-storage
```

#### Package Installation Failures
```bash
pkg update && pkg upgrade
pkg install python git curl wget
```

#### Python Command Not Found
In Termux, use `python` instead of `python3`:
```bash
python GoOsint.py -e target@gmail.com
```

#### SSL Certificate Errors
```bash
pkg install ca-certificates
```

#### Memory Issues on Low-End Devices
- Close other apps to free memory
- Use single email investigation instead of batch processing
- Consider using a more powerful device for large investigations

## 📝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

This project is for educational purposes only. Please use responsibly and in accordance with applicable laws and regulations.

## 🙏 Acknowledgments

- **GHunt**: The core OSINT engine powering this tool
- **Colorama**: For beautiful terminal colors
- **Python Community**: For excellent libraries and support

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review GHunt documentation
3. Create an issue in the repository

---

**Remember: With great power comes great responsibility. Use GoOsint ethically and legally.**
